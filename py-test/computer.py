#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-02-24 11:19:52
# @Author  : XieXianbin (a.b@hotmail.com)
# @Link    : http://www.zzidc.com
# @Version : 1.0

import resultcode
from commons import utils, log, openapi_endpoint_type, power, openapi_param, openapi_version,\
    openapiconfinfo,db   #=20150119=
from service.flavors import flavors
from commons.loopcall import _loop  #=20150119=
from service.image import image
from service.blockstorage import blockstorage
from service.networking import networking
from config import CHECK_COUNTS, PER_TIMES
import time

class computer(object):
    tokens = None
    computer_endpoints = None
    tokenId = None

    def __init__(self, tokens=None):
        """
        initialization tokens
        """
        self.tokens = tokens
        if self.tokens:
            self.computer_endpoints = utils.get_endpoints_bytype(self.tokens["endpoints"], openapi_endpoint_type.COMPUTER)
            self.tokenId = str(self.tokens["tokenId"])

    """public method"""
    """instance manager"""
    def create_instance(self, hostname, region, image_id, cpu, ram, disk, bandwidth, adminPass=None, network_name=None, uuid=None, port=None, \
                        accessIPv4=None, fixed_ip=None, accessIPv6=None, security_group=None, user_data=None, \
                        availability_zone=None, metadata={}, personality=[]):
        """
        create a new instance. 
        """ 
        try: 
            # 1. get imageRef(an image manager URL) by image id.
            imag_o = image(tokens=self.tokens)
            return_state, return_body = imag_o.get_image_url_by_id(image_id=image_id)
            # judge invoke value 
            if return_state:
                # 1.1 success  
                log.debug('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), get the special imageRef success.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "uuid": uuid, "port": port, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality})
                imageRef = return_body
            else:
                # 1.2 fail 
                if "IMAGE_NOT_FOUND":
                    log.warn('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), Can not got special images by id. IMAGE_NOT_FOUND.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "uuid": uuid, "port": port, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality})
                    return (resultcode.ImageNotFound, None)
                else: 
                    log.warn('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), got images list fail. return_body: %(return_body)s.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "return_body": return_body})
                    return (resultcode.BadRequest, "GET_IMAGES_LIST_FAIL")
            # 2. get the special flavor by configure, If it is not exits, Create a new one. 
            flavor_o = flavors(tokens=self.tokens)
            return_state, return_body = flavor_o.get_flavor_by_config(cpu=cpu, ram=ram, disk=disk, bandwidth=bandwidth)
            if return_state: 
                # 2.1 success, get flavor id 
                log.debug('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), get the special flavorRef success. This may be new create. return_body: %(return_body)s.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "return_body": return_body})
                flavorRef = return_body["id"]
            else: 
                # 2.2 fail, get flavor detail by id 
                log.warn('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), got flavor id fail. return_body: %(return_body)s.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "return_body": return_body})
                return (resultcode.FlavorInvalid, return_body)
            # 3. get network UUID by network name 
            if uuid is None:
                network_o = networking(tokens=self.tokens)
                return_state, return_body = network_o.get_network_uuid_by_name(network_name=network_name)
                if return_state:
                    # success 
                    log.debug("METHOD: create_instance_with_block_device_mapping(), get network uuid by network id success.")
                    uuid = return_body
                else:
                    # fail 
                    log.warn("METHOD: create_instance_with_block_device_mapping(), get network uuid by network id fail. return_body: %(return_body)s." % {"return_body": return_body})
                    return (resultcode.BadRequest, return_body)
            else: 
                # use the special UUID 
                pass
            # 4. invoke private method to create an new instance release by image, and the instance DOES NOT attachment volume. 
            return_state, return_body = self.__create_instance(flavorRef=flavorRef, imageRef=imageRef, name=hostname, adminPass=adminPass, uuid=uuid, port=port, accessIPv4=accessIPv4, fixed_ip=fixed_ip, accessIPv6=accessIPv6, security_group=security_group, user_data=user_data, availability_zone=availability_zone, metadata=metadata, personality=personality)
            # 4.1 judge return value 
            if return_state: 
                # success
                log.info('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), create instance successful. return_body: %(return_body)s.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "return_body": return_body})
                instance_id = return_body["server"]["id"]
                adminPass = return_body["server"]["adminPass"]
                return (resultcode.Success, {"instance_id": instance_id, "adminPass": adminPass})
            else:
                # fail 
                log.warn('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), create instance fail. return_body: %(return_body)s.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "return_body": return_body})
                return (resultcode.CreateInsanceFailed, return_body)
        except Exception, e:
            log.error('METHOD: create_instance(hostname=%(hostname)s, adminPass=%(adminPass)s, region=%(region)s, image_id=%(image_id)s, cpu=%(cpu)d, ram=%(ram)d, disk=%(disk)d, bandwidth=%(bandwidth)d, network_name=%(network_name)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), When create instance occur an Exception: %(e)s.' % {"adminPass": adminPass, "hostname": hostname, "region": region, "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def create_instance_with_block_device_mapping(self, name, region, systen_volume_id, os_type,\
            image_id, cpu, ram, disk, bandwidth, network_name=None, uuid=None, port=None, data_volume_id=None, security_group=None, user_data=None, \
            availability_zone=None, fixed_ip=None, metadata={}, personality=[], adminPass=None, delete_on_termination=True):
        """
        Creates a server with a block device mapping.
        """
        try:
            # 1. judge image is or is not exist 
            image_o = image(tokens=self.tokens)
            return_state, return_body = image_o.get_image_url_by_id(image_id=image_id)
            # judge return values 
            if return_state:
                # the special image is exist 
                log.debug("METHOD: create_instance_with_block_device_mapping(name=%(name)s, adminPass=%(adminPass)s, region=%(region)s, systen_volume_id=%(systen_volume_id)s, os_type=%(os_type)s, data_volume_id=%(data_volume_id)s, image_id=%(image_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, fixed_ip=%(fixed_ip)s, metadata=%(metadata)s, personality=%(personality)s, delete_on_termination=%(delete_on_termination)s), get the special image success."
                    % {"name": name, "adminPass": adminPass, "region": region, "systen_volume_id": systen_volume_id, "os_type": os_type, "data_volume_id": data_volume_id, \
                    "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "uuid": uuid, "port": port, "security_group": security_group, "user_data": user_data, \
                    "availability_zone": availability_zone, "fixed_ip": fixed_ip, "metadata": metadata, "personality": personality, "delete_on_termination": delete_on_termination})
                imageRef = image_id
                pass
            else:
                # not found 
                log.warn("METHOD: create_instance_with_block_device_mapping(name=%(name)s, adminPass=%(adminPass)s, region=%(region)s, systen_volume_id=%(systen_volume_id)s, os_type=%(os_type)s, data_volume_id=%(data_volume_id)s, image_id=%(image_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, fixed_ip=%(fixed_ip)s, metadata=%(metadata)s, personality=%(personality)s, delete_on_termination=%(delete_on_termination)s), Could not found the special image, return_body: %(return_body)s."
                    % {"name": name, "adminPass": adminPass, "region": region, "systen_volume_id": systen_volume_id, "os_type": os_type, "data_volume_id": data_volume_id, \
                    "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "network_name": network_name, "bandwidth": bandwidth, "uuid": uuid, "port": port, "security_group": security_group, "user_data": user_data, \
                    "availability_zone": availability_zone, "fixed_ip": fixed_ip, "metadata": metadata, "personality": personality, "delete_on_termination": delete_on_termination, "return_body": return_body})
                return (resultcode.ImageNotFound, return_body)
            # 2. get the special flavor by configure, If it is not exits, Create a new one.
            flavor_o = flavors(tokens=self.tokens)
            return_state, return_body = flavor_o.get_flavor_by_config(cpu=cpu, ram=ram, disk=disk, bandwidth=bandwidth)
            # judge the return values 
            if return_state:
                log.debug("METHOD: create_instance_with_block_device_mapping(), get flavor success.")
                flavorRef = return_body["id"]
            else:
                log.warn("METHOD: create_instance_with_block_device_mapping(), get flavor fail.")
                return (resultcode.BadRequest, return_body)
            # 3. get network uuid by network name 
            if uuid is None:
                network_o = networking(tokens=self.tokens)
                return_state, return_body = network_o.get_network_uuid_by_name(network_name=network_name)
                if return_state:
                    # success 
                    log.debug("METHOD: create_instance_with_block_device_mapping(), get network uuid by network id success.")
                    uuid = return_body
                else:
                    log.warn("METHOD: create_instance_with_block_device_mapping(), get network uuid by network id fail. return_body: %(return_body)s." % {"return_body": return_body})
                    return (resultcode.BadRequest, return_body)
            else:
                # use uuid
                pass
            # 3. invoke private method to create an instance with block device mapping 
            return_state, return_body = self.__create_instance_with_block_device_mapping(name=name, adminPass=adminPass, \
                                                    region=region, systen_volume_id=systen_volume_id, os_type=os_type, data_volume_id=data_volume_id, \
                                                    imageRef=imageRef, flavorRef=flavorRef, uuid=uuid, port=port, \
                                                    security_group=security_group, user_data=user_data, \
                                                    availability_zone=availability_zone, fixed_ip=fixed_ip, metadata=metadata, \
                                                    personality=personality, delete_on_termination=delete_on_termination)
            # judge the return values 
            if return_state:
                # create success
                log.info("METHOD: create_instance_with_block_device_mapping(name=%(name)s, adminPass=%(adminPass)s, region=%(region)s, systen_volume_id=%(systen_volume_id)s, os_type=%(os_type)s, data_volume_id=%(data_volume_id)s, image_id=%(image_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, fixed_ip=%(fixed_ip)s, metadata=%(metadata)s, personality=%(personality)s, delete_on_termination=%(delete_on_termination)s), Create instance success. return_body: %(return_body)s."
                    % {"name": name, "adminPass": adminPass, "region": region, "systen_volume_id": systen_volume_id, "os_type": os_type, "data_volume_id": data_volume_id, \
                    "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "uuid": uuid, "port": port, "security_group": security_group, "user_data": user_data, \
                    "availability_zone": availability_zone, "fixed_ip": fixed_ip, "metadata": metadata, "personality": personality, "delete_on_termination": delete_on_termination, "return_body": return_body})
                # filter links
#                return_body["server"].pop("links")
                instance_id = return_body["server"]["id"]
                # return server id 
                return (resultcode.Success, {"instance_id": instance_id})
            else: 
                # create fail 
                log.warn("METHOD: create_instance_with_block_device_mapping(name=%(name)s, adminPass=%(adminPass)s, region=%(region)s, systen_volume_id=%(systen_volume_id)s, os_type=%(os_type)s, data_volume_id=%(data_volume_id)s, image_id=%(image_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, fixed_ip=%(fixed_ip)s, metadata=%(metadata)s, personality=%(personality)s, delete_on_termination=%(delete_on_termination)s), Create instance fail. return_body: %(return_body)s."
                    % {"name": name, "adminPass": adminPass, "region": region, "systen_volume_id": systen_volume_id, "os_type": os_type, "data_volume_id": data_volume_id, \
                    "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "network_name": network_name, "bandwidth": bandwidth, "uuid": uuid, "port": port, "security_group": security_group, "user_data": user_data, \
                    "availability_zone": availability_zone, "fixed_ip": fixed_ip, "metadata": metadata, "personality": personality, "delete_on_termination": delete_on_termination, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
        except Exception, e: 
            log.error("METHOD: create_instance_with_block_device_mapping(name=%(name)s, adminPass=%(adminPass)s, region=%(region)s, systen_volume_id=%(systen_volume_id)s, os_type=%(os_type)s, data_volume_id=%(data_volume_id)s, image_id=%(image_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s, network_name=%(network_name)s, uuid=%(uuid)s, port=%(port)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, fixed_ip=%(fixed_ip)s, metadata=%(metadata)s, personality=%(personality)s, delete_on_termination=%(delete_on_termination)s), When Create instance Occur an Exception: %(e)s."
                % {"name": name, "adminPass": adminPass, "region": region, "systen_volume_id": systen_volume_id, "os_type": os_type, "data_volume_id": data_volume_id, \
                "image_id": image_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "network_name": network_name, "uuid": uuid, "port": port, "security_group": security_group, "user_data": user_data, \
                "availability_zone": availability_zone, "fixed_ip": fixed_ip, "metadata": metadata, "personality": personality, "delete_on_termination": delete_on_termination, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def delete_instance(self, instance_id):
        """
        delete instance. 
        NOTIC: this method will delete instance from volume permanent, Could not be restore again.
        Status Transition: ACTIVE -> DELETED or ERROR -> DELETED or SHUTOFF->DELETED
        This operation deletes a specified cloud server instance from the system.
        """
        try:
            # 1. get instance detail
            return_state, return_body = self.__get_instance_details(instance_id)
            # judge instance is or is not exist
            if not return_state:
                # not exist
                log.warn('METHOD: delete_instance(instance_id=%(instance_id)s), The instance could not be found.' % {"instance_id": instance_id})
                return (resultcode.InstanceNotFound, None)
            elif return_body["server"]["status"] != "ACTIVE" and return_body["server"]["status"] != "ERROR" and return_body["server"]["status"] != "SHUTOFF":
                # 2.2 instance is exist, judge the state, if it is ACTIVE or ERROR or SHUTOFF, delete. Or not allow to operation
                log.warn("METHOD: (instance_id=%(instance_id)s), The instance, which is in an active or error state, could be delete. But this instance is in the wrong state: %(state)s." % {"instance_id": instance_id, "state": return_body["server"]["status"]})
                return (resultcode.InstanceOperateFailed, "THIS_INSTANCE_IS_NOT_IN_AN_ACTIVE_OR_ERROR_OR_SHUTOFF_STATE")
            # 3. build URL
            url = self.__get_compute_base_url() + "/servers/" + instance_id
            # 4. invoke OpenStack API to delete the special server forever
            response_state, response_body = utils.deleteapi(url=url, token=self.tokenId)
            # 5. judge the response values
            if response_state:
                # success
                log.info('METHOD: delete_instance(instance_id=%(instance_id)s), delete instance success.' % {"instance_id": instance_id})
                return (resultcode.Success, response_body)
            else:
                log.warn('METHOD: delete_instance(instance_id=%(instance_id)s), delete instance fail. response_body: %(response_body)s' % {"instance_id": instance_id, "response_body": response_body})
                return (resultcode.InstanceOperateFailed, response_body)
        except Exception, e:
            log.error('METHOD: delete_instance(instance_id=%(instance_id)s), when delete instance occur an exception: %(e)s' % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def resize_instance(self, instance_id, cpu, ram, disk, bandwidth):
        """
        Resizes the specified server. 
        """
	log.debug("resize_instance "+instance_id)
        try:
            # 1. judge the special instance is or is not exist
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            if return_state:
                # exist 
                log.debug("METHOD: resize_instance(instance_id=%(instance_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s), Found the special instance success." % {"instance_id": instance_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth})
                pass
            else:
                # not exist 
                log.warn("METHOD: resize_instance(instance_id=%(instance_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s), Could not Found the special instance. return_body: %(return_body)s." % {"instance_id": instance_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "return_body": return_body})
                return (resultcode.InstanceNotFound, return_body)
            # 2. get flavorRef by instance configure
            flavor_o = flavors(tokens=self.tokens)
            return_state, return_body = flavor_o.get_flavor_by_config(cpu=cpu, ram=ram, disk=disk, bandwidth=bandwidth)
            if return_state:
                # success 
                flavorRef = return_body["id"]
            else:
                # fail 
                log.warn("METHOD: resize_instance(instance_id=%(instance_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s), Got flavorRef fail. return_body: %(return_body)s." % {"instance_id": instance_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
            # 3. invoke inner method to resize the special instance
            return_state, return_body = self.resize_instance_inner(instance_id=instance_id, flavorRef=flavorRef)
            if return_state:
                # success 
                log.info("METHOD: resize_instance(instance_id=%(instance_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s), resize instance success. return_body: %(return_body)s." % {"instance_id": instance_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail 
                log.warn("METHOD: resize_instance(instance_id=%(instance_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s), resize instance fail. return_body: %(return_body)s." % {"instance_id": instance_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
        except Exception, e:
            log.error("METHOD: resize_instance(instance_id=%(instance_id)s, cpu=%(cpu)s, ram=%(ram)s, disk=%(disk)s, bandwidth=%(bandwidth)s), When resize instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "cpu": cpu, "ram": ram, "disk": disk, "bandwidth": bandwidth, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def confirm_resize_instance(self, instance_id):
        """
        Confirms a pending resize action. 
        """
        try:
            # 1. invoke inner method to confirms a pending resize
            return_state, return_body =  self.confirm_resize_instance_inner(instance_id=instance_id)
            # judge return values
            if return_state:
                # success
                log.info("METHOD: confirm_resize_instance(instance_id=%(instance_id)s), confirm instance success. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail
                log.warn("METHOD: confirm_resize_instance(instance_id=%(instance_id)s), confirm instance fail. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceOperateFailed, return_body)
        except Exception, e:
            log.error("METHOD: confirm_resize_instance(instance_id=%(instance_id)s), When confirm resize Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def rebuild_instance(self, instance_id, imageRef, name, adminPass, accessIPv4, accessIPv6, metadata, personality):
        """
        Rebuilds the specified server. 
        Specify the rebuild action in the request body.
        """
        try:
            # 1. judge instance is or is not exist 
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            if return_state:
                log.debug("METHOD: rebuild_instance(instance_id=%(instance_id)s), Found the special instance success." % {"instance_id": instance_id})
                pass
            else:
                log.warn("METHOD: rebuild_instance(instance_id=%(instance_id)s), instance can not be found. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, None)
            # 2. build URL
            url = self.__get_compute_base_url() + "/servers/" + instance_id + "/action"
            # 3. build request body
            request_body = openapi_param.get_rebuild_instance_param(imageRef=imageRef, name=name, adminPass=adminPass, accessIPv4=accessIPv4, accessIPv6=accessIPv6, metadata=metadata, personality=personality)
            # 4. invoke OpenStack API to rebuild the special instance 
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # judge response value 
            if response_state:
                # success
                log.info("METHOD:rebuild_instance(instance_id=%(instance_id)s), instance rebuild success. response_body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                response_body["server"].pop("links")
                response_body["server"]["image"].pop("links")
                response_body["server"]["flavor"].pop("links")
                return (resultcode.Success, response_body)
            else:
                # fail
                log.warn("METHOD:rebuild_instance(instance_id=%(instance_id)s), instance rebuild fail. response_body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (resultcode.InstanceOperateFailed, response_body)
        except Exception, e:
            log.error("METHOD:rebuild_instance(instance_id=%(instance_id)s), when rebuild instance occur an exception: %(e)s" % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    ### 测试未通过
    def force_delete_instance(self, instance_id):
        """
        Force-deletes a server.
        """
        if self.tokens:
            try:
                # 1. 获取实例
                temp_vm = self.__get_instance_detail(instance_id)
                # 2. 判断实例是否存在
                if not temp_vm:
                    log.warn('METHOD:force_delete_instance("%(instance_id)s"), The instance can not be found.' % {"instance_id": instance_id})
                    return (resultcode.InstanceNotFound, None)
                # 3. 构造URL
                url = str(self._ + instance_id + "/action")
                log.debug(url)
                # 4. 构造request body
                request_body = {"forceDelete": None}
                # 5. 调用接口
                resp_state, resp_body = utils.deleteapi(url, par=request_body, token=self.tokenId)
                if resp_state:
                    log.info('METHOD:force_delete_instance("%(instance_id)s"), force delete instance success.' % {"instance_id": instance_id})
                    return (resultcode.Success, None)
                else:
                    log.warn('METHOD:force_delete_instance("%(instance_id)s"), force delete instance fail. resp_body: %(resp_body)s' % {"instance_id": instance_id, "resp_body": resp_body})
                    return (resultcode.InstanceOperateFailed, resp_body)
            except Exception, e:
                log.error('METHOD:force_delete_instance("%(instance_id)s"), when force delete an instance occur an exception: %(e)s' % {"instance_id": instance_id, "e": e})
                log.exception(e)
                return (resultcode.ServerError, e)
        else:
            log.error("METHOD:force_delete_instance('%(instance_id)s'), The token is disabled." % {"instance_id": instance_id})
            return (resultcode.Frobidden, None)
    
    ### 测试未通过
    def restores_force_delete_instance(self, instance_id):
        """
        Restores a deleted server.
        """
        try:
            # 1. 构造URL
            url = str(self.__get_compute_servers_url() + "/" + instance_id + "/action")
            log.debug(url)
            # 2. 构造request body
            request_body = {"restore": None}
            # 3. 调用接口
            resp_code, resp_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 4. 处理返回值
            if resp_code:
                log.info('METHOD:restores_force_delete_instance("%(instance_id)s"), restores instance success.' % {"instance_id": instance_id})
                return (resultcode.Success, None)
            else:
                log.warn('METHOD:restores_force_delete_instance("%(instance_id)s"), restores instance fail. resp_body: %(resp_body)s' % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.InstanceOperateFailed, resp_body)
        except Exception, e:
            log.error('METHOD:restores_force_delete_instance("%(instance_id)s"), when restores a delete instance occur an exception: %(e)s.' % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, None)
    
    def change_instance_password(self, instance_id, adminPass):
        """
        Changes the password for a server. Specify the changePassword action in the request body.
        """
        try:
            # 1. 判断实例是否存在
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            if return_state:
                # 存在
                log.debug("METHOD: change_instance_password(instance_id=%(instance_id)s, adminPass=%(adminPass)s), find instance success." % {"instance_id": instance_id, "adminPass": adminPass})
                pass
            else:
                log.warn("METHOD: change_instance_password(instance_id=%(instance_id)s, adminPass=%(adminPass)s), Could Not find the special instance. return_body: %(return_body)s." % {"instance_id": instance_id, "adminPass": adminPass, "return_body": return_body})
                return (resultcode.InstanceNotFound, return_body)
            # 2. 调用接口
            resp_state, resp_body = self.__change_instance_password(instance_id=instance_id, adminPass=adminPass)
            # 3. 处理返回值
            if resp_state:
                # 3.1 成功
                log.info('METHOD:change_instance_password(instance_id=%(instance_id)s, adminPass=%(adminPass)s), change password success. resp_body: %(resp_body)s.' % {"instance_id": instance_id, "adminPass": adminPass, "resp_body": resp_body})
                return (resultcode.Success, resp_body)
            else:
                # 3.2 失败
                log.warn('METHOD:change_instance_password(instance_id=%(instance_id)s, adminPass=%(adminPass)s), change password fail. resp_body: %(resp_body)s.' % {"instance_id": instance_id, "adminPass": adminPass, "resp_body": resp_body})
                return (resultcode.BadRequest, resp_body)
        except Exception, e:
            log.error('METHOD:change_instance_password(instance_id=%(instance_id)s, adminPass="%(adminPass)s), when change instance password occur an exception: %(e)s.' % {"instance_id": instance_id, "adminPass": adminPass, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    """instance power manager"""
    def start_instance(self, instance_id):
        """
        start a special instance. 
        """
        try:
            # 1.获取虚拟机
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            # 2.判断虚拟机是否存在
            if not return_state:
                log.warn("METHOD:start_instance(instance_id=%(instance_id)s), instance can not be found or is on ERROR status. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, return_body)
            # 3.判断虚拟机的电源状态 
            isstart = power.isStart(self.__get_instance_power_status(return_body["server"]))
            if not isstart:
                log.warn("METHOD:start_instance(instance_id=%(instance_id)s), instance is already started. Can't be started again." % {"instance_id": instance_id})
                return (resultcode.NotAllowed,  "WAS_STARTED_OR_ERROR")
            # 4. 构造URL
            url = str(return_body["server"]["links"][0]["href"] + "/action")
            # 5. 构造request_body 
            request_body = {"os-start": None}
            # 6. 调用接口 
            resp_code, resp_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 7. 处理返回值
            if resp_code:
                log.info("METHOD:start_instance(instance_id=%(instance_id)s), instance is started success." % {"instance_id": instance_id})
                return (resultcode.Success, resp_body)
            else:
                log.warn("METHOD:start_instance(instance_id=%(instance_id)s), instance started fail. response body: %(request_body)s." % {"instance_id": instance_id, "request_body": request_body})
                return (resultcode.InstanceOperateFailed, resp_body)
        except Exception, e:
            log.error("METHOD:start_instance(instance_id=%(instance_id)s), when start instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def stop_instance(self, instance_id):
        """
        stop a special instance 
        """
        try:
            # 1. 获取虚拟机实例
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            # 2. 判断机器是否存在
            if not return_state:
                log.warn("METHOD:stop_instance(instance_id=%(instance_id)s), instance  can not be found. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, None)
            # 3. 判断虚拟机的电源状态
            isShutOff = power.isShutOff(self.__get_instance_power_status(return_body["server"]))
            if not isShutOff:
                log.warn("METHOD:stop_instance(instance_id=%(instance_id)s), instance is already stopped or is on ERROR status. Can't be stopped." % {"instance_id": instance_id})
                return (resultcode.NotAllowed, "WAS_STOPED_OR_ERROR")
            # 4. 构造URL
            url = str(return_body["server"]["links"][0]["href"] + "/action")
            # 5 构造request_body 
            request_body = {"os-stop": None}
            # 6. 调用接口
            resp_state, resp_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 7. 处理返回值
            if resp_state:
                log.info("METHOD:stop_instance(instance_id=%(instance_id)s), instance is stopped success. resp_body: %(resp_body)s." % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.Success, resp_body)
            else:
                log.warn("METHOD:stop_instance(instance_id=%(instance_id)s), instance is stopped fail. response body: %(resp_body)s" % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.InstanceOperateFailed, resp_body)
        except Exception, e:
            log.error("METHOD:stop_instance(instance_id=%(instance_id)s), when stop instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def soft_reboot_instance(self, instance_id):
        """
        soft软重启实例：开始运行里重启电脑
        ACTIVE -> REBOOT -> ACTIVE (soft reboot)
        SOFT. The operating system is signaled to restart, which allows for a graceful shutdown of all processes.
        """
        try:
            # 1. 获取实例
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            # 2. 判断实例是否存在
            if not return_state:
                log.warn("METHOD:soft_reboot_instance(instance_id=%(instance_id)s), instance can not be found. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, return_body)
            # 3. 构造URL 
            url = str(return_body["server"]["links"][0]["href"] + "/action")
            # 4. 构造request body 
            requers_body = {"reboot" : {"type" : "SOFT"}}
            # 5. 调用接口，软重启实例 
            resp_state, resp_body = utils.postapi(url=url, par=requers_body, token=self.tokenId)
            # 6. 处理返回值
            if resp_state:
                log.info("METHOD:soft_reboot_instance(instance_id=%(instance_id)s), instance is rebooted success. resp_body: %(resp_body)s." % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.Success, resp_body)
            else:
                log.warn("METHOD:soft_reboot_instance(instance_id=%(instance_id)s), instance is rebooted fail. response body: %(resp_body)s." % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.InstanceOperateFailed, resp_body)
        except Exception, e:
            # 7. 处理异常
            log.error("METHOD:soft_reboot_instance(instance_id=%(instance_id)s), when soft reboot instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def hard_reboot_instance(self, instance_id):
        """
        hard硬重启实例：实例断电后重新启动
        ACTIVE -> HARD_REBOOT -> ACTIVE (hard reboot)
        HARD. Equivalent to power cycling the server.
        """
        try:
            # 1. 获取实例
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            # 2. 判断实例是否存在 
            if not return_state:
                log.warn("METHOD:hard_reboot_instance(instance_id=%(instance_id)s), instance can not be found. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, return_body)
            # 3. 构造URL 
            url = str(return_body["server"]["links"][0]["href"] + "/action")
            # 4. 构造request body
            request_body = {"reboot" : {"type" : "HARD"}}
            # 5. 调用接口，硬重启实例
            resp_state, resp_body = utils.postapi(url, request_body, token=self.tokenId)
            # 6. 处理返回值
            if resp_state:
                log.info("METHOD:hard_reboot_instance('%(instance_id)s'), instance is rebooted success. resp_body: %(resp_body)s." % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.Success, resp_body)
            else:
                log.warn("METHOD:hard_reboot_instance('%(instance_id)s'), instance is rebooted fail. response body: %(resp_body)s" % {"instance_id": instance_id, "resp_body": resp_body})
                return (resultcode.InstanceOperateFailed, resp_body)
        except Exception, e:
            log.error("METHOD:hard_reboot_instance('%(instance_id)s'), when hard reboot instance Occur an Exception: %(e)s" % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    """instance details"""
    def list_instance(self):
        """
        get instance list for special tenant
        """
        try:
            # 1. 获取实例列表
            instance_list_return = self.__get_instance_list_detail()
            # 2. 格式化处理
            if instance_list_return[0]:
                instance_list = []
                for item in instance_list_return[1]:
                    instance_list.append(self.__get_instance_busdetail(item))
                # 3.1 处理返回值
                log.debug(instance_list)
                dic = {}
                dic["instance_count"] = len(instance_list)
                dic["instance_list"] = instance_list
                log.debug(dic)
                return (resultcode.Success, dic)
            else:
                # 3.2 处理失败返回值
                log.warn("METHON:list_instance(), get instance list fail. response body: %(resp_boyd)s" % {"resp_boyd": instance_list_return[1]})
                return (resultcode.BadRequest, instance_list_return[1]) 
        except Exception, e:
            log.error("METHOD:list_instance(), when get instance list occur an exception: %(e)s." % {"e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def describe_instance(self, instance_id):
        """
        get the special instance details
        """
        try:
            # 1. get instance details
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            # 2. judge the instance is or is not exist 
            if return_state:
                log.debug("METHOD:describe_instance(instance_id='%(instance_id)s'), Found the special instance success. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
            else:
                log.warn("METHOD:describe_instance(instance_id='%(instance_id)s'), the special instance can not be found. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, None)
            # 3. 获取指定实例的详细信息
            instance_busdetail = self.__get_instance_busdetail(pinstance_detail=return_body)
            # 4. 处理返回值
            return (resultcode.Success, instance_busdetail["server"])
        except Exception, e:
            log.error('METHON:describe_instance(instance_id="%(instance_id)s"), when got an instance describe occurred an exception: %(e)s' % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def vnc_console(self, instance_id, vnc_type):
        """
        Gets a console for a server instance.
        vnc_type: Valid values are novnc and xvpvnc.
        """
        try:
            # 1. build URL
            url = self.__get_compute_base_url() + "/servers/" + instance_id + "/action"
            # 2. build request body
            request_body = openapi_param.get_vnc_console_parm(vnc_type=vnc_type)
            # 3. invoke OpenStack API
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 4. judge return value
            if response_state:
                # success
                log.debug("METHOD: vnc_console(instance_id=%(instance_id)s, vnc_type=%(vnc_type)s), get instance VNC console success. response_body: %(response_body)s." % {"instance_id": instance_id, "vnc_type": vnc_type, "response_body": response_body})
                return (resultcode.Success, {"vnc_url": response_body["console"]["url"]})
            else:
                # fail
                log.warn("METHOD: vnc_console(instance_id=%(instance_id)s, vnc_type=%(vnc_type)s), get instance VNC console fail. response_body: %(response_body)s." % {"instance_id": instance_id, "vnc_type": vnc_type, "response_body": response_body})
                return (resultcode.BadRequest, response_body)
        except Exception, e:
            log.error("METHOD: vnc_console(instance_id=%(instance_id)s, vnc_type=%(vnc_type)s), When get instance VNC console Occur an Exception: %(e)s." % {"instance_id": instance_id, "vnc_type": vnc_type, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    """manager instance volume"""
    def list_volume_attachment_for_instance(self, instance_id):
        """
        Lists the volume attachments for a specified server.
        """
        try:
            # 1. invoke inner method
            return_state, return_body = self.list_volume_attachment_for_instance_inner(instance_id=instance_id)
            # 2. judge return value
            if return_state:
                log.debug("METHOD: list_volume_attachment_for_instance(instance_id=%(instance_id)s), get success. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                log.warn("METHOD: list_volume_attachment_for_instance(instance_id=%(instance_id)s), get fail. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceOperateFailed, return_body)
        except Exception, e:
            log.error("METHOD: list_volume_attachment_for_instance(instance_id=%(instance_id)s), When get volumes list Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    # 测试成功， 暂不对外提供 
    def attachment_new_volume_to_instance(self, instance_id, size, description=None, name=None):
        """attachment a volume to an instance"""
        try:
            # 1. 获取实例
            return_state, return_body = self.__get_instance_details(instance_id)
            # 2. 判断实例是否存在
            if return_state is False:
                # 2.1 实例不存在
                log.warn("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s), Could not found the special instance. return_body: %(return_body)s." % {"instance_id": instance_id, "return_body": return_body})
                return (resultcode.InstanceNotFound, return_body)
            else:
                # 2.2 实例存在
                pass
            # 3. create a new volume 
            blockstorage_o = blockstorage(tokens=self.tokens)
            return_state, return_body = blockstorage_o.create_volume_inner(size=size, availability_zone=None, source_volid=None, description=description, snapshot_id=None, name=name, imageRef=None, volume_type=None, bootable=False, metadata=None)
            # 3.1 judge invoke result
            if return_state:
                log.debug("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), create a new volume success. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                # 3.1.1 get the new volume id 
                volume_id = return_body["volume"]["id"]
                # 3.1.2 judge volume state 
                for i in range(CHECK_COUNTS):
                    time.sleep(PER_TIMES)
                    # 3.1.2.1 get volume detail
                    return_state, return_body = blockstorage_o.get_volume_by_id(volume_id=volume_id)
                    if return_state:
                        volume_state = return_body["volume"]["status"]
                        if volume_state == "available":
                            # success 
                            log.debug("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), get new create volume's state is available. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                            break
                        elif volume_state == "error":
                            # fail
                            log.warn("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), get new create volume's state is error. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                            return (resultcode.BadRequest, return_body)
                    else:
                        log.warn("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), get the new volume detail fail. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                        return (resultcode.BadRequest, return_body)
                if i >= CHECK_COUNTS:
                    log.warn("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), the special volume has been deleted." % {"instance_id": instance_id, "size": size, "description": description, "name": name})
                    return (resultcode.BadRequest, "THE_VOLUME_HAS_BEEN_DELETED")
            else:
                log.warn("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), When create a new volume fail. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
            # 4. attachment an new create volume to the special instance 
            return_state, return_body = self.attachment_volume_to_instance_inner(instance_id=instance_id, volumeId=volume_id)
            if return_state:
                # success
                log.info("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), attach a new volume to instance success. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail
                log.warn("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), attach a new volume to instance fail. return_body: %(return_body)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
        except Exception, e:
            log.exception("METHOD: attachment_new_volume_to_instance(instance_id=%(instance_id)s, size=%(size)s, description=%(description)s, name=%(name)s), When attach a new volume to instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "size": size, "description": description, "name": name, "e": e})
            log.error(e)
            return (resultcode.ServerError, e)
    
    def attachment_volume_to_instance(self, instance_id, volumeId):
        """attach a exits volume to the special instance"""
        try:
            # 1. attach volume to instance
            return_state, return_body = self.attachment_volume_to_instance_inner(instance_id=instance_id, volumeId=volumeId)
            if return_state:
                # success
                log.info("METHOD: attachment_volume_to_instance(instance_id=%(instance_id)s, volumeId=%(volumeId)s), attach an exits volume to instance success. return_body: %(return_body)s." % {"instance_id": instance_id, "volumeId": volumeId, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail
                log.warn("METHOD: attachment_volume_to_instance(instance_id=%(instance_id)s, volumeId=%(volumeId)s), attach an exits volume to instance fail. return_body: %(return_body)s." % {"instance_id": instance_id, "volumeId": volumeId, "return_body": return_body})
                return (resultcode.InstanceOperateFailed, return_body)
        except Exception, e:
            log.error("METHOD: attachment_volume_to_instance(instance_id=%(instance_id)s, volumeId=%(volumeId)s), when attach an exits volume to instance occur an Exception: %(e)s." % {"instance_id": instance_id, "volumeId": volumeId, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def delete_volume_from_instance(self, instance_id, attachment_id):
        """
        Deletes the specified volume attachment from a specified server.
        attachment_id: The id of the special volume which will delete from the special instance.
        """
        try:
            # 1. invoke inner method
            return_state, return_body = self.delete_volume_from_instance_inner(instance_id=instance_id, attachment_id=attachment_id)
            # 2. judge return value
            if return_state:
                log.info("METHOD: delete_volume_from_instance(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), operate success. return_body: %(return_body)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                log.warn("METHOD: delete_volume_from_instance(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), operate fail. return_body: %(return_body)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "return_body": return_body})
                if return_body == "InstanceNotFound":
                    return (resultcode.InstanceNotFound, return_body)
                else:
                    return (resultcode.InstanceOperateFailed, return_body)
        except Exception, e:
            log.error("METHOD: delete_volume_from_instance(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), operate fail. return_body: %(e)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    """IP manager"""
    # 获取floating IP 方法，使用及返回值待定
    def list_os_floating_ips(self):
        """获取与项目或用户相关联的floating IP"""
        """Lists floating IP addresses associated with the tenant or account."""
        try:
            # 1. 获取URL
            url = self.computer_endpoints["publicURL"] + "/os-floating-ips"
            log.debug(url)
            # 2. 调用方法
            resp_state, resp_body = utils.getapi(url=url, token=self.tokenId)
            # 3. 处理返回值
            if resp_state:
                log.debug("METHOD: list_os_floating_ips(), get instance IP list success. resp_body: %(resp_body)s." % {"resp_body": resp_body})
                return (resultcode.Success, resp_body)
            else:
                log.error("METHOD: list_os_floating_ips(), get instance IP list fail. resp_body: %(resp_body)s." % {"resp_body": resp_body})
                return (resultcode.BadRequest, resp_body)
        except Exception, e:
            log.error("METHOD: list_os_floating_ips(), When get instance IP list occur an Exception. e: %(e)s." % {"e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def allocate_floating_ip(self, pool):
        """
        Allocates a new floating IP address to a tenant or account. 
        """
        try:
            # 1. invoke inner method to allocate a new floating IP 
            return_state, return_body = self.allocate_floating_ip_inner(pool=pool)
            # 2. judge result 
            if return_state:
                # success
                log.info("METHOD: allocate_floating_ip(pool=%(pool)s), allocate floating ip success. return_body: %(return_body)s." % {"pool": pool, "return_body": return_body})
                return (resultcode.Success, return_body["floating_ip"])
            else:
                # fail
                log.warn("METHOD: allocate_floating_ip(pool=%(pool)s), allocate floating ip fail. return_body: %(return_body)s." % {"pool": pool, "return_body": return_body})
                return (resultcode.NoMoreFloatingIps, return_body)
        except Exception, e:
            log.error("METHOD: allocate_floating_ip(pool=%(pool)s), When Allocate Floating ip Occur an Exceptin: %(e)s." % {"pool": pool, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def deallocates_floating_ip(self, ip_id, address):
        """
        Deallocates the floating IP address associated with floating_IP_address_ID. 
        """
        try:
            # 0. if ip_id is None, get ip_id by address. 
            if ip_id is None:
                return_state, return_body = self.get_floatingIp_id_by_address(address=address)
                if return_state:
                    log.debug("METHOD: deallocates_floating_ip(ip_id=%(ip_id)s, address=%(address)s), get floating ip id success. return_body: %(return_body)s." % {"ip_id": ip_id, "address": address, "return_body": return_body})
                    ip_id = return_body 
                else:
                    log.warn("METHOD: deallocates_floating_ip(ip_id=%(ip_id)s, address=%(address)s), deallocate fail. return_body: %(return_body)s." % {"ip_id": ip_id, "address": address, "return_body": return_body})
                    return (resultcode.BadRequest, return_body)
            else:
                pass
            # 1. invoke inner method to deallocate floating ip from tehant 
            return_state, return_body = self.deallocates_floating_ip_inner(ip_id=ip_id)
            # 2. judge response values
            if return_state:
                # success
                log.info("METHOD: deallocates_floating_ip(ip_id=%(ip_id)s, address=%(address)s), deallocate success. return_body: %(return_body)s." % {"ip_id": ip_id, "address": address, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail
                log.warn("METHOD: deallocates_floating_ip(ip_id=%(ip_id)s, address=%(address)s), deallocate fail. return_body: %(return_body)s." % {"ip_id": ip_id, "address": address, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
        except Exception, e:
            log.error("METHOD: deallocates_floating_ip(ip_id=%(ip_id)s, address=%(address)s), When deallocate floating ip Occur an Exception: %(e)s." % {"ip_id": ip_id, "address": address, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def add_floatingIp_to_instance(self, instance_id, address, fixed_address=None):
        """
        Adds a floating IP address to an instance.
        fixed_address: A fixed IP address that you want to associate with the floating IP address.
        address: A floating IP address to associate with the instance.
        """
        try:
            # 1. invoke inner method to add floating ip to instance 
            return_state, return_body = self.add_floatingIp_to_instance_inner(instance_id=instance_id, address=address, fixed_address=fixed_address)
            # judge response values 
            if return_state:
                # success 
                log.info("METHOD: add_floatingIp_to_instance(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), add a floating IP to instance success. return_body: %(return_body)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail 
                log.warn("METHOD: add_floatingIp_to_instance(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), add a floating IP to instance fail. return_body: %(return_body)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "return_body": return_body})
                if return_body == "InstanceNotFound":
                    # Could not found the special instance 
                    return (resultcode.InstanceNotFound, return_body)
                else:
                    return (resultcode.BadRequest, return_body)
        except Exception, e:
            log.error("METHOD: add_floatingIp_to_instance(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), When add a floating IP to instance occur an exception: %(e)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    def removes_floating_ip_from_instance(self, instance_id, address):
        """
        Removes a floating IP from an instance. 
        """
        try:
            # 1. invoke inner method to remove the special floating ip from instance 
            return_state, return_body = self.removes_floating_ip_from_instance_inner(instance_id=instance_id, address=address)
            # judge result values
            if return_state:
                # success
                log.info("METHOD: removes_floating_ip_from_instance(instance_id=%(instance_id)s, address=%(address)s), remove success. return_body: %(return_body)s." % {"instance_id": instance_id, "address": address, "return_body": return_body})
                return (resultcode.Success, return_body)
            else:
                # fail 
                log.warn("METHOD: removes_floating_ip_from_instance(instance_id=%(instance_id)s, address=%(address)s), remove fail. return_body: %(return_body)s." % {"instance_id": instance_id, "address": address, "return_body": return_body})
                return (resultcode.BadRequest, return_body)
        except Exception, e:
            log.error("METHOD: removes_floating_ip_from_instance(instance_id=%(instance_id)s, address=%(address)s), When remove Occur an Exception: %(e)s." % {"instance_id": instance_id, "address": address, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
    # 未知是否使用 方法未完成。。。。
    def injects_network_info_into_instance(self):
        """
        Injects network information into a server.
        """
        try:
            
            
            
            pass
        except Exception, e:
            log.error("")
            log.exception(e)
    
    """Rules for security group (os-security-group-rules)"""
    def create_security_group_rule(self, security_group_id, name, ip_protocol, from_port, to_port, cidr):
        """
        Creates a security group rule
        """
        try: 
            # 0. judge from_port and to_port 
            if from_port > to_port:
                log.warn("METHOD: create_security_group_rule(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), Former value cannot be greater than the later." \
                         % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr})
                return (resultcode.BadRequest, "Former value cannot be greater than the later")
            else:
                pass
            # 1. invoke inner method to create security group rule 
            return_state, return_body = self.create_security_group_rule_inner(security_group_id=security_group_id, name=name, ip_protocol=ip_protocol, from_port=from_port, to_port=to_port, cidr=cidr)
            # judge return values 
            if return_state:
                # success 
                log.info("METHOD: create_security_group_rule(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), create rule success." \
                         % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr})
                return (resultcode.Success, return_body)
            else:
                # fail 
                log.warn("METHOD: create_security_group_rule(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), create rule fail." \
                         % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr})
                return (resultcode.BadRequest, return_body)
            pass
        except Exception, e:
            log.error("METHOD: create_security_group_rule(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), When create rule Occur an Exception: %(e)s." \
                     % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e)
    
#    def deletes_security_group_rule(self):
#        """
#        Deletes a specified security group rule. 
#        """
#        pass
    
    """inner method"""
    """innver method of volume"""
    def list_volume_attachment_for_instance_inner(self, instance_id):
        """
        Lists the volume attachments for a specified server.
        """
        try:
            # 1. build URL
            url = self.__get_compute_servers_url() + "/" + instance_id + "/os-volume_attachments"
            # 2. invoke OpenStack method
            response_state, response_body = utils.getapi(url=url, token=self.tokenId)
            # 3. judge response volume
            if response_state:
                # success
                log.debug("METHOD: list_volume_attachment_for_instance_inner(instance_id=%(instance_id)s), get success. response_body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (True, response_body)
            else:
                # fail
                log.debug("METHOD: list_volume_attachment_for_instance_inner(instance_id=%(instance_id)s), get fail. response_body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: list_volume_attachment_for_instance_inner(instance_id=%(instance_id)s), When get instance attachments list Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            raise e
    
    def attachment_volume_to_instance_inner(self, instance_id, volumeId):
        """
        attach a volume to special instance
        """
        try:
            # 1. 构造URL
            url = self.__get_compute_servers_url() + "/" + instance_id + "/os-volume_attachments"
            # 2. 构造request body
            request_body = openapi_param.get_attachment_volume_to_instance_inner_parm(volumeId=volumeId)
            # 3. 调用接口
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 4. 处理返回值
            if response_state:
                # 4.1 成功
                log.info("METHOD:attachment_volume_to_instance_inner(instance_id=%(instance_id)s, volumeId=%(volumeId)s), attachment volume to instance success. response_body: %(response_body)s." % {"instance_id": instance_id, "volumeId": volumeId, "response_body": response_body})
                return (True, response_body)
            else:
                # 4.2 失败
                log.warn("METHOD:attachment_volume_to_instance_inner(instance_id=%(instance_id)s, volumeId=%(volumeId)s), attachment volume to instance fail. response_body: %(response_body)s." % {"instance_id": instance_id, "volumeId": volumeId, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD:attachment_volume_to_instance_inner(instance_id=%(instance_id)s, volumeId=%(volumeId)s), When attachment a volume to instance occur an Exception: %(e)s." % {"instance_id": instance_id, "volumeId": volumeId, "e": e})
            log.exception(e)
            raise e
    
    # Shows details for the specified volume attachment. 
    
    def delete_volume_from_instance_inner(self, instance_id, attachment_id):
        """
        Deletes the specified volume attachment from a specified server.
        attachment_id: The id of the special volume which will delete from the special instance.
        """
        try:
            # 1. judge instance is or is not exist
            return_state, return_body = self.__get_instance_details(instance_id=instance_id)
            if return_state:
                # instance is exist
                log.debug("METHOD: delete_volume_from_instance_inner(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), found The Special instance success." % {"instance_id": instance_id, "attachment_id": attachment_id})
                pass
            else:
                # fail 
                log.warn("METHOD: delete_volume_from_instance_inner(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), The special instance is not exist. return_body: %(return_body)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "return_body": return_body})
                return (False, "InstanceNotFound")
            # 1. build URL 
            url = self.__get_compute_servers_url() + "/" + instance_id + "/os-volume_attachments/" + attachment_id
            # 2. invoke OpenStack API
            response_state, response_body = utils.deleteapi(url=url, token=self.tokenId)
            # 3. judge result value
            if response_state:
                # success
                log.info("METHOD: delete_volume_from_instance_inner(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), delete the special volume from instance success. response_body: %(response_body)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "response_body": response_body})
                return (True, response_body)
            else:
                # fail
                log.warn("METHOD: delete_volume_from_instance_inner(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), delete the special volume from instance fail. response_body: %(response_body)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: delete_volume_from_instance_inner(instance_id=%(instance_id)s, attachment_id=%(attachment_id)s), When delete the special volume from instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "attachment_id": attachment_id, "e": e})
            log.exception(e)
            raise e
    
    """inner method of instance"""
    def resize_instance_inner(self, instance_id, flavorRef):
        """
        Resizes the specified server. 
        Specify the resize action in the request body. 
        """
        try:
            # 1. build invoke URL
            url = self.__get_compute_servers_url() + "/" + instance_id + "/action"
            # 2. build request body
            request_body = openapi_param.get_resize_instance_inner_param(flavorRef=flavorRef)
            # 3. invoke OpenStack method
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # judge response result
            if response_state:
                # success
                log.info("METHOD: resize_instance_inner(instance_id=%(instance_id)s, flavorRef=%(flavorRef)s), resize success. response_body: %(response_body)s." % {"instance_id": instance_id, "flavorRef": flavorRef, "response_body": response_body})
                return (True, response_body)
            else:
                # fail
                log.warn("METHOD: resize_instance_inner(instance_id=%(instance_id)s, flavorRef=%(flavorRef)s), resize fail. response_body: %(response_body)s." % {"instance_id": instance_id, "flavorRef": flavorRef, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: resize_instance_inner(instance_id=%(instance_id)s, flavorRef=%(flavorRef)s), When resize The Special Instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "flavorRef": flavorRef, "e": e})
            log.exception(e)
            raise e
    
    def confirm_resize_instance_inner(self, instance_id):
        """
        Confirms a pending resize action. 
        Specify the confirmResize action in the request body.
        """
        try:
            # 1. build invoke URL
            url = self.__get_compute_servers_url() + "/" + instance_id + "/action"
            # 2. build request body 
            request_body = openapi_param.get_confirm_resize_instance_inner_param()
            # 3. invoke OpenStack interface
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # judge response result
            if response_state:
                # success
                log.info("METHOD: confirm_resize_instance_inner(instance_id=%(instance_id)s), confirm resize instance success. response_body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (True, response_body)
            else:
                # fail
                log.warn("METHOD: confirm_resize_instance_inner(instance_id=%(instance_id)s), confirm resize instance fail. response_body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: confirm_resize_instance_inner(instance_id=%(instance_id)s), When confirm resize instance Occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            raise e
    
    def get_instance_detail(self, instance_id):
        """get instance's detail"""
        try:
            # 1. 获取URL
            url = str(self.__get_compute_base_url() + "/servers/" + instance_id)
            # 2. 调用接口
            response_state, response_body = utils.getapi(url=url, token=self.tokenId)
            # 3. 处理返回值
            if response_state:
                log.debug("METHOD: get_instance_detail(instance_id=%(instance_id)s), get instance detail success. response body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (True, response_body)
            else:
                log.warn("METHOD: get_instance_detail(instance_id=%(instance_id)s), get instance detail fail. response body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                return (False, response_body)
        except Exception, e: 
            log.error("METHOD: get_instance_detail(instance_id=%(instance_id)s), When get instance detail occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            raise e 
    
    """inner method of IPs"""
    def allocate_floating_ip_inner(self, pool):
        """
        Allocates a new floating IP address to a tenant or account.
        This may be has some relation with get token method, but I'am not insure?????
        """
        try:
            # 1. build URL
            url = self.__get_compute_base_url() + "/os-floating-ips"
            # 2. build request body
            request_body = openapi_param.get_allocate_floating_ip_parm(pool=pool)
            # 3. invoke Openstack API to allocate a new floating IP address to the special tenant or account
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 4. judge response result 
            if response_state:
                # allocate new floating ip success
                log.info("METHOD: allocate_floating_ip_inner(pool=%(pool)s), allocates new floating ip success. response_body: %(response_body)s." % {"pool": pool, "response_body": response_body})
                return (True, response_body)
            else:
                log.warn("METHOD: allocate_floating_ip_inner(pool=%(pool)s), allocates new floating ip fail. response_body: %(response_body)s." % {"pool": pool, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: allocate_floating_ip_inner(pool=%(pool)s), When allocates a new floating to the special tenant or account Occur An Exception: %(e)s." % {"pool": pool, "e": e})
            log.exception(e)
            raise e
    
    def deallocates_floating_ip_inner(self, ip_id):
        """
        Deallocates the floating IP address associated with floating_IP_address_ID.
        """
        try:
            # 1. build URL
            url = self.__get_compute_base_url() + "/os-floating-ips/" + ip_id
            # 2. invoke OpenStack API to deallocate floating ip from the specials tenant
            response_state, response_body = utils.deleteapi(url=url, token=self.tokenId)
            # 3. judge response result 
            if response_state:
                # success 
                log.info("MEHOD: deallocates_floating_ip_inner(ip_id=%(ip_id)s), deallocate floating ip from the specials tenant success. response_body: %(response_body)s." % {"ip_id": ip_id, "response_body": response_body})
                return (True, response_body)
            else:
                # fail 
                log.warn("MEHOD: deallocates_floating_ip_inner(ip_id=%(ip_id)s), deallocate floating ip from the specials tenant fail. response_body: %(response_body)s." % {"ip_id": ip_id, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("MEHOD: deallocates_floating_ip_inner(ip_id=%(ip_id)s), When deallocate floating ip from the specials tenant Occur an Exception: %(e)s." % {"ip_id": ip_id, "e": e})
            log.exception(e)
            raise e
    
    def add_floatingIp_to_instance_inner(self, instance_id, address, fixed_address=None):
        """
        Adds a floating IP address to an instance.
        fixed_address: A fixed IP address that you want to associate with the floating IP address.
        address: A floating IP address to associate with the instance.
        """
        try:
            # 1. judge the instance is or is not exists 
            return_state, retrun_body = self.__get_instance_details(instance_id=instance_id)
            if return_state is False:
                log.warn("METHOD: add_floatingIp_to_instance_inner(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), The instance can not be found. retrun_body: %(retrun_body)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "retrun_body": retrun_body})
                return (False, "InstanceNotFound")
            # 2. 判断IP是否可用??
            pass
            
            # 3. build URL
            url = self.__get_compute_servers_url() + "/" + instance_id + "/action"
            # 4. build request body 
            request_body = openapi_param.get_add_floatingIp_to_instance_param(address=address, fixed_address=fixed_address)
            # 5. invoke OpenStack API to add the special floating ip to the instance 
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            # 6. judge result values 
            if response_state:
                # allocate success 
                log.info("METHOD: add_floatingIp_to_instance_inner(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), add a floating IP to instance success. response_body: %(response_body)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "response_body": response_body})
                return (True, response_body)
            else: 
                # allocate fail 
                log.warn("METHOD: add_floatingIp_to_instance_inner(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), add a floating IP to instance fail. response_body: %(response_body)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: add_floatingIp_to_instance_inner(instance_id=%(instance_id)s, address=%(address)s, fixed_address=%(fixed_address)s), When add a floating IP to instance occur an exception: %(e)s." % {"instance_id": instance_id, "address": address, "fixed_address": fixed_address, "e": e})
            log.exception(e)
            raise e
    
    def removes_floating_ip_from_instance_inner(self, instance_id, address):
        """
        Removes a floating IP from an instance. 
        """ 
        try:
            # 1. build URL
            url = self.__get_compute_servers_url() + "/" + instance_id + "/action"
            # 2. build request body 
            request_body = openapi_param.get_removes_a_floating_ip_param(address=address)
            # 3. invoke OpenStack API to removes the special floting ip from instance 
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId)
            if response_state:
                log.info("METHOD: removes_floating_ip_from_instance_inner(instance_id=%(instance_id)s, address=%(address)s), remove the special floating ip from instance success. response_body: %(response_body)s." \
                         % {"instance_id": instance_id, "address": address, "response_body": response_body})
                return (True, response_body)
            else:
                log.warn("METHOD: removes_floating_ip_from_instance_inner(instance_id=%(instance_id)s, address=%(address)s), remove the special floating ip from instance fail. response_body: %(response_body)s." \
                         % {"instance_id": instance_id, "address": address, "response_body": response_body})
                ####       2014-4-18                                                 ###
                ####       The type of response_body is str, not dict.               ###
                log.debug(type(response_body))
                return (False, eval(response_body))
        except Exception, e:
            log.error("METHOD: removes_floating_ip_from_instance_inner(instance_id=%(instance_id)s, address=%(address)s), When remove the special floating ip from instance Occur an Exception: %(e)s." \
                      % {"instance_id": instance_id, "address": address, "e": e})
            log.exception(e)
            raise e
    
    def get_floatingIp_list(self):
        """
        Lists floating IP addresses associated with the tenant or account. 
        """
        try:
            # 1. build URL 
            url = self.__get_compute_base_url() + "/os-floating-ips"
            # 2. invoke OpenStack API to get floating IP lists. 
            response_state, response_body = utils.getapi(url=url, token=self.tokenId) 
            # judge response values 
            if response_state:
                # success 
                log.debug("METHOD: get_floatingIp_list(), get floatingIP list success. response_body: %(response_body)s." % {"response_body": response_body})
                return (True, response_body)
            else:
                # fail 
                log.warn("METHOD: get_floatingIp_list(), get floatingIP list fail. response_body: %(response_body)s." % {"response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: get_floatingIp_list(), When get floatingIP Occur an Exception: %(e)s." % {"e": e})
            log.exception(e)
            raise e
    
    def get_floatingIp_id_by_address(self, address):
        """
        get floating ip id by Ip-address. 
        """
        try: 
            # 1. get floating IP list 
            return_state, return_body = self.get_floatingIp_list() 
            # judge return values 
            if return_state: 
                # list floating Ip success 
                log.debug("METHOD: get_floatingIp_id_by_address(address=%(address)s), get floating ip list success. return_body: %(return_body)s." % {"address": address, "return_body": return_body})
                floating_ips = return_body["floating_ips"]
                for i in range(len(floating_ips)): 
                    # get the special floating ip 
                    floating_ip = floating_ips[i]
                    if floating_ip["ip"] == address:
                        # get it 
                        log.debug("METHOD: get_floatingIp_id_by_address(address=%(address)s), get the special floating ip success. floating_ip: %(floating_ip)s." % {"address": address, "floating_ip": floating_ip})
                        return (True, floating_ip["id"])
                    else:
                        continue
                log.warn("METHOD: get_floatingIp_id_by_address(address=%(address)s), the special floating ip Could not be found. return_body: %(return_body)s." % {"address": address, "return_body": return_body})
                return (False, "FLOATING_IP_NOT_FOUND")
            else: 
                # fail 
                log.warn("METHOD: get_floatingIp_id_by_address(address=%(address)s), get floating ip list fail. return_body: %(return_body)s." % {"address": address, "return_body": return_body})
                return (False, return_body)
        except Exception, e:
            log.error("METHOD: get_floatingIp_id_by_address(address=%(address)s), When the special floating ip Occur an Exceptin: %(e)s." % {"address": address, "e": e})
            log.exception(e)
            raise e
    
    """inner method: Security groups (os-security-groups)"""
    def list_security_groups_inner(self):
        """
        Lists security groups. 
        """
        try:
            # 1. build URL 
            url = self.__get_compute_base_url() + "/os-security-groups"
            # 2. invoke OpenStack API to list security groups 
            response_state, response_body = utils.getapi(url=url, token=self.tokenId)
            # judge response values 
            if response_state:
                # success 
                log.debug("METHOD: list_security_groups_inner(), list success. response_body: %(response_body)s." % {"response_body": response_body})
                return (True, response_body)
            else:
                # fail 
                log.warn(("METHOD: list_security_groups_inner(), list fail. response_body: %(response_body)s." % {"response_body": response_body}))
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: list_security_groups_inner(), When list security group Occur An Exception: %(e)s." % {"e": e})
            log.exception(e)
            raise e
    
    def get_security_group_by_name(self, name):
        """
        get security group by name 
        """
        try:
            # 1. get security groups list 
            return_state, return_body = self.list_security_groups_inner()
            # 2. judge response values 
            if return_state:
                # success 
                log.debug("METHOD: get_security_group_by_name(name=%(name)s), get sucurity groups list success." % {"name": name})
                security_groups = return_body["security_groups"]
                # list security groups 
                for i in range(len(return_body)):
                    group = security_groups[i]
                    if group["name"] == name:
                        # find the special security group success
                        return (True, group)
                    else:
                        # not match 
                        continue
                return (False, None)
            else:
                log.warn("METHOD: get_security_group_by_name(name=%(name)s), get sucurity groups list fail. return_body: %(return_body)s." % {"name": name, "return_body": return_body})
                return (False, return_body)
        except Exception, e:
            log.error("METHOD: get_security_group_by_name(name=%(name)s), When get sucurity groups Occur an Exception: %(e)s." % {"name": name, "e": e})
            log.exception(e)
            raise e
    
    """inner method: Rules for security group (security_group_rule)"""
    def create_security_group_rule_inner(self, security_group_id, name, ip_protocol, from_port, to_port, cidr):
        """
        Creates a default security group rule.
        """
        try:
            if security_group_id is None:
                # 1. get security group by name 
                return_state, return_body = self.get_security_group_by_name(name=name)
                # judge return values 
                if return_state:
                    # success
                    log.debug("METHOD: create_security_group_rule_inner(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), get security group by name success." \
                              % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr}) 
                    security_group_id = return_body["id"]
                    pass
                else: 
                    # fail 
                    log.debug("METHOD: create_security_group_rule_inner(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), get security group by name fail. return_body: %(return_body)s." \
                              % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr, "return_body": return_body})
                    return (False, return_body)
            else:
                pass
            # 2. build URL 
            url = self.__get_compute_base_url() + "/os-security-group-rules"
            # 3. build request_body 
            request_body = openapi_param.get_create_security_group_rule_inner_param(group_id=None, parent_group_id=security_group_id, ip_protocol=ip_protocol, from_port=from_port, to_port=to_port, cidr=cidr)
            # 4. invoke OpenStack API to create security group roule 
            response_state, response_body = utils.postapi(url=url, par=request_body, token=self.tokenId) 
            # judge response values 
            if response_state: 
                # success 
                log.info("METHOD: create_security_group_rule_inner(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), create roule success. response_body: %(response_body)s." \
                         % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr, "response_body": response_body})
                return (True, response_body)
            else: 
                # fail 
                log.warn("METHOD: create_security_group_rule_inner(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), create roule fail. response_body: %(response_body)s." \
                         % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: create_security_group_rule_inner(security_group_id=%(security_group_id)s, name=%(name)s, ip_protocol=%(ip_protocol)s, from_port=%(from_port)s, to_port=%(to_port)s, cidr=%(cidr)s), When create roule Occur an Exception: %(e)s." \
                      % {"security_group_id": security_group_id, "name": name, "ip_protocol": ip_protocol, "from_port": from_port, "to_port": to_port, "cidr": cidr, "e": e})
            log.exception(e)
            raise e

    """inner Quota sets (os-quota-sets)"""
    def updates_nova_quotas_inner(self, tenant_id, cores, fixed_ips, floating_ips, injected_file_content_bytes, \
                            injected_file_path_bytes, injected_files, instances, key_pairs, \
                            metadata_items, ram, security_group_rules, security_groups):
        """
        Updates quotas for a tenant.
        Compute API v2 extensions
        """
        try: 
            # 1. build URL 
            url = self.__get_compute_base_url() + "/os-quota-sets/" + tenant_id
            # 2. build request parameter
            request_body = openapi_param.get_updates_nova_quotas_inner_param(cores=cores, fixed_ips=fixed_ips, floating_ips=floating_ips, injected_file_content_bytes=injected_file_content_bytes, injected_file_path_bytes=injected_file_path_bytes, injected_files=injected_files, instances=instances, key_pairs=key_pairs, metadata_items=metadata_items, ram=ram, security_group_rules=security_group_rules, security_groups=security_groups)
            # 3. invoke OpenStack API to update nova quotas parameters 
            response_state, response_body = utils.putapi(url=url, par=request_body, token=self.tokenId)
            # judge response values 
            if response_state:
                # quotas success 
                log.info("METHOD: updates_nova_quotas_inner(tenant_id=%(tenant_id)s, cores=%(cores)s, fixed_ips=%(fixed_ips)s, floating_ips=%(floating_ips)s, injected_file_content_bytes=%(injected_file_content_bytes)s, injected_file_path_bytes=%(injected_file_path_bytes)s, injected_files=%(injected_files)s, instances=%(instances)s, key_pairs=%(key_pairs)s, metadata_items=%(metadata_items)s, ram=%(ram)s, security_groups=%(security_groups)s, security_group_rules=%(security_group_rules)s), update nova quotas success. response_body: %(response_body)s." \
                         % {"tenant_id": tenant_id, "cores": cores, "fixed_ips": fixed_ips, "floating_ips": floating_ips, "injected_file_content_bytes": injected_file_content_bytes, "injected_file_path_bytes": injected_file_path_bytes, "injected_files": injected_files, "instances": instances, "key_pairs": key_pairs, "metadata_items": metadata_items, "ram": ram, "security_groups": security_groups, "security_group_rules": security_group_rules, "response_body": response_body})
                return (True, response_body)
            else: 
                # fail 
                log.warn("METHOD: updates_nova_quotas_inner(tenant_id=%(tenant_id)s, cores=%(cores)s, fixed_ips=%(fixed_ips)s, floating_ips=%(floating_ips)s, injected_file_content_bytes=%(injected_file_content_bytes)s, injected_file_path_bytes=%(injected_file_path_bytes)s, injected_files=%(injected_files)s, instances=%(instances)s, key_pairs=%(key_pairs)s, metadata_items=%(metadata_items)s, ram=%(ram)s, security_groups=%(security_groups)s, security_group_rules=%(security_group_rules)s), update nova quotas fail. response_body: %(response_body)s." \
                         % {"tenant_id": tenant_id, "cores": cores, "fixed_ips": fixed_ips, "floating_ips": floating_ips, "injected_file_content_bytes": injected_file_content_bytes, "injected_file_path_bytes": injected_file_path_bytes, "injected_files": injected_files, "instances": instances, "key_pairs": key_pairs, "metadata_items": metadata_items, "ram": ram, "security_groups": security_groups, "security_group_rules": security_group_rules, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: updates_nova_quotas_inner(tenant_id=%(tenant_id)s, cores=%(cores)s, fixed_ips=%(fixed_ips)s, floating_ips=%(floating_ips)s, injected_file_content_bytes=%(injected_file_content_bytes)s, injected_file_path_bytes=%(injected_file_path_bytes)s, injected_files=%(injected_files)s, instances=%(instances)s, key_pairs=%(key_pairs)s, metadata_items=%(metadata_items)s, ram=%(ram)s, security_groups=%(security_groups)s, security_group_rules=%(security_group_rules)s), When update nova quotas Occur an Exception: %(e)s." \
                      % {"tenant_id": tenant_id, "cores": cores, "fixed_ips": fixed_ips, "floating_ips": floating_ips, "injected_file_content_bytes": injected_file_content_bytes, "injected_file_path_bytes": injected_file_path_bytes, "injected_files": injected_files, "instances": instances, "key_pairs": key_pairs, "metadata_items": metadata_items, "ram": ram, "security_groups": security_groups, "security_group_rules": security_group_rules, "e": e})
            log.exception(e)
            raise e
        
    def disable_host_service(self,host_name,binary_name):
        """
        host_name:主机名称
        binary_name:主机二进制名称
        Disables scheduling for a service.计算节点服务停用
        """
        try:
            #1.build URL
            url = self.__get_compute_base_url() + "/os-services/disable"
            # 2. build request parameter
            request_body=openapi_param.get_updates_disable_host_service_param(host_name=host_name,binary_name=binary_name)
            # 3. invoke OpenStack API to disable_host_service  parameters 
            response_state, response_body=utils.putapi(url=url, par=request_body, token=self.tokenId)
            # judge response values 
            if response_state:
                # disable hosts service  success 
                log.info("METHOD:disable_host_service(host_name=%(host_name)s,binary_name=%(binary_name)s, disable host services success. response_body: %(response_body)s." \
                         % {"host_name":host_name, "binary_name": binary_name, "response_body": response_body})
                return (True, response_body)
            else: 
                # disable hosts service 
                log.info("METHOD:disable_host_service(host_name=%(host_name)s,binary_name=%(binary_name)s, disable host services fail. response_body: %(response_body)s." \
                         % {"host_name":host_name, "binary_name": binary_name, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD:disable_host_service(host_name=%(host_name)s,binary_name=%(binary_name)s, disable host services fail. response_body: %(response_body)s." \
                          % {"host_name":host_name, "binary_name": binary_name,"response_body": response_body, "e": e})
            log.exception(e)
            raise e 
        
    def  instance_list_belong_to_hypervisor(self,host_name):
        """
        hypervisor_hostname:hypervisor名称
        find instance list by host_name
        """
        try:
            #1.build URL
            url = self.__get_compute_base_url() + "/os-hypervisors/"+host_name+"/servers"
            #2. invoke OpenStack API to instance_list_belong_to_hypervisor find instance lists parameters 
            response_state, response_body=utils.getapi(url=url, token=self.tokenId)

            # judge response values 
            if response_state:
            # find instances list success 
                log.info("METHOD:instance_list_belong_to_hypervisor(host_name=%(host_name)s, find instances list  success. response_body: %(response_body)s." \
                     % {"host_name":host_name, "response_body": response_body})
                return (True, response_body)
            else: 
            # find instances list fail 
                log.info("METHOD:instance_list_belong_to_hypervisor(host_name=%(host_name)s, find instances list  fail. response_body: %(response_body)s." \
                    % {"host_name":host_name, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD:instance_list_belong_to_hypervisor(host_name=%(host_name)s, find instances list  fail. response_body: %(response_body)s." \
                     % {"host_name":host_name,"response_body": response_body, "e": e})
            log.exception(e)
            raise e

    def  hot_live_migration(self,server_id,block_migration,disk_over_commit,dest_host):
        """
         hot live migration 热迁移
        """
        try:
            #1.build URL
            url = self.__get_compute_servers_url() +"/"+server_id+"/action"
            # 2. build request parameter
            request_body=openapi_param.get_updates_hot_live_migration_param(host=dest_host,block_migration=block_migration,disk_over_commit=disk_over_commit)
            #3. invoke OpenStack API to hot_live_migration parameters 
            response_state, response_body=utils.postapi(url=url, par=request_body,token=self.tokenId)
            # judge response values 
            if response_state:
            # hot live migration success 
                log.info("METHOD:hot_live_migration(server_id=%(server_id)s,block_migration=%(block_migration)s,disk_over_commit=%(disk_over_commit)s,dest_host=%(dest_host)s, hot live migration success. response_body: %(response_body)s." \
                     % {"server_id":server_id, "block_migration": block_migration, "disk_over_commit": disk_over_commit, "dest_host": dest_host, "response_body": response_body})
                return (True, response_body)
            else: 
            # hot live migration fail 
                log.info("METHOD:hot_live_migration(server_id=%(server_id)s,block_migration=%(block_migration)s,disk_over_commit=%(disk_over_commit)s,dest_host=%(dest_host)s, hot live migration fail. response_body: %(response_body)s." \
                     % {"server_id":server_id, "block_migration": block_migration, "disk_over_commit": disk_over_commit, "dest_host": dest_host, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD:hot_live_migration(server_id=%(server_id)s,block_migration=%(block_migration)s,disk_over_commit=%(disk_over_commit)s,dest_host=%(dest_host)s, hot live migration fail. response_body: %(response_body)s." \
                     % {"server_id":server_id, "block_migration": block_migration, "disk_over_commit": disk_over_commit, "dest_host": dest_host, "response_body": response_body, "e": e})
            log.exception(e)
            raise e
        
    def  cold_live_migration(self,server_id):
        """
        cold live migration 冷迁移
        """
        try:
            #1.build URL
            url = self.__get_compute_servers_url() +"/"+server_id+"/action"
            # 2. build request parameter
            request_body=openapi_param.get_updates_cold_live_migration_param()
            #3. invoke OpenStack API to cold_live_migration parameters 
            response_state, response_body=utils.postapi(url=url, par=request_body,token=self.tokenId)
            # judge response values 
            if response_state:
            # cold live migration success 
                log.info("METHOD:cold_live_migration(server_id=%(server_id)s,cold live migration success. response_body: %(response_body)s." \
                    % {"server_id":server_id, "response_body": response_body})
                return (True, response_body)
            else: 
            # cold live migration fail 
                log.info("METHOD:cold_live_migration(server_id=%(server_id)s,cold live migration fail. response_body: %(response_body)s." \
                    % {"server_id":server_id, "response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD:cold_live_migration(server_id=%(server_id)s,cold live migration fail. response_body: %(response_body)s." \
                    % {"server_id":server_id,"response_body": response_body,"e": e})
            log.exception(e)
            raise e   
         
    def host_migration(self,origin_host,binary_name,dest_host,instance_list,is_close_coupute_node):
        """
        orgin_host:源主机
        dest_host:目标主机
        host migration计算节点上的虚拟机迁移
        """
        try:
            #1 enable hosts service关闭计算节点服务
            if is_close_coupute_node:
                result,body=self.disable_host_service(host_name=origin_host,binary_name=binary_name)
            else :
                result=True;
            #2 result is true,next is select hypervisor's instances
            if result:
                #hyp_result,hyp_response_body=self.instance_list_belong_to_hypervisor(host_name=origin_host)

                #3 hyp_result is true,next is find instance details
                #if hyp_result:
                if instance_list:
                    try:
                        #instance_list=hyp_response_body["hypervisors"][0]["servers"]
                        instance_list=list(instance_list.split("+"))
                    except Exception,e:
                        instance_list=None
                        log.info("the hypervisor's instances is null")
                    if instance_list:
                        for instance_id in instance_list:
                            #instance_id=element["uuid"]
                            ins_result,ins_response_body=self.get_instance_detail(instance_id=instance_id)
                            #4 ins_result is true,next is judge instance's status
                            if ins_result:
                                current_instance_status=ins_response_body["server"]["status"]
                                #5.1 instance's status is ACTIVE,use the hot migration
                                if current_instance_status=="ACTIVE":
                                    liv_result,liv_response_body=self.hot_live_migration(server_id=instance_id,block_migration=False,disk_over_commit=False,dest_host=dest_host)
                                    if liv_result:
                                        log.info("This instance is success to hot live migration")
                                    else:
                                        log.info("This instance is failure to hot live migration---%s"% liv_response_body)     
                                #5.2 instance's status is SHUTOFF,use the cold live migration
                                else:
                                    col_result,col_response_body=self.cold_live_migration(server_id=instance_id)
                                    if col_result:
                                        log.info("This instance is success to cold live migration")
                                    else:
                                        log.info("This instance is failure to cold live migration---%s"% col_response_body)
                                        #return(resultcode.BadRequest,col_response_body)  
                            else:
                                log.info("Fail to fin instance by uuid---%s"% instance_id)
                                return(resultcode.BadRequest,ins_response_body)
                        
                        return(resultcode.Success,{})
                    else:
                        return(resultcode.NotFoundInstance,body)
                else:
                    log.info("Fail to select hypervisior's instances")
                    
                    return(resultcode.BadRequest,body)
            else:
                log.info("Fail to disable hosts")
                return(resultcode.BadRequest,body)
        except Exception,e:
            log.error("Fail to migrate host's instance")
            log.exception(e)
            raise e   

    """nova服务宿主机列表"""         
    def nova_hosts_list(self):
        try:
            #1 build url
            url = self.__get_compute_base_url() + "/os-services"
            #2 invoke OpenStack API to show hosts 
            response_state, response_body=utils.getapi(url=url,token=self.tokenId)
            # judge response values 
            if response_state:
                log.info("METHOD:nova_hosts_list(),show hosts success. response_body: %(response_body)s." \
                    % { "response_body": response_body})
                return (resultcode.Success, response_body)
            else:
                log.info("METHOD:nova_hosts_list(),show hosts fail. response_body: %(response_body)s." \
                    % { "response_body": response_body})
                return (resultcode.BadRequest, response_body)
             
        except Exception,e:
            log.error("Fail to show hosts")
            log.exception(e)
            raise e
        
    """private method"""
    def __get_compute_base_url(self):
        """
        get computer 操作的基本方法
        http://192.168.12.154:8774/v2/fa89f2643d004627a8eea7d395ad6c8d
        """
        return str(self.computer_endpoints["publicURL"])
    
    def __get_compute_servers_url(self):
        """
        get compute servers url
        e.g. http://192.168.12.154:8774/v2/fa89f2643d004627a8eea7d395ad6c8d/servers
        """
        return str(self.computer_endpoints["publicURL"] + "/servers")
    
    def __get_instance_list_detail(self):
        """获取实例列表详细信息,return list<dict>"""
        try:
            resp_code, vm_list = utils.getapi(self.computer_endpoints[
                "publicURL"] + "/servers/detail", token=self.tokenId)
            if resp_code:
                return (True, vm_list["servers"])
            else:
                log.warn("METHOD:__get_instance_list_detail(), get instance list fail. response body: %(vm_list)s." % {"vm_list": vm_list})
                return (False, vm_list)
        except Exception, e:
            log.warn("METHOD:__get_instance_list_detail(), When get instance list occur an exception: %(e)s." % {"e": e})
            log.exception(e)
            raise e
    
    def __get_instance_power_status(self, pinstance_detail):
        if pinstance_detail:
            return pinstance_detail.get("status")
    
    def __is_start_instance(self, now_statue=None):
        pass
    
    def __get_instance_detail(self, instance_id):
        """获取指定实例详细信息,return dict，私有方法"""
        try:
            if instance_id:
                url = self.__get_compute_servers_url() + "/" + instance_id
                resp_state, temp_vm_info = utils.getapi(url=url, token=self.tokenId)
                if resp_state:
                    return temp_vm_info["server"]
                else:
                    log.warn("METHOD: __get_instance_detail(instance_id=%(instance_id)s), get special instance detail fail. response body: %(temp_vm_info)s." % {"instance_id": instance_id, "temp_vm_info": temp_vm_info})
                    return None
        except Exception, e:
            log.error("METHOD: __get_instance_detail(instance_id=%(instance_id)s), When get instance detail occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            raise e
    
    def __get_instance_details(self, instance_id):
        """
        get the special instance detail. 
        Compare with the __get_instance_detail() method, it's return value will contain two values. 
        """
        try:
            if instance_id:
                url = self.__get_compute_servers_url() + "/" + instance_id
                response_state, response_body = utils.getapi(url=url, token=self.tokenId)
                if response_state:
                    log.debug("METHOD: __get_instance_details(instance_id=%(instance_id)s), get special instance detail success. response body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                    return (True, response_body)
                else:
                    log.warn("METHOD: __get_instance_details(instance_id=%(instance_id)s), get special instance detail fail. response body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                    return (False, response_body)
        except Exception, e:
            log.error("METHOD: __get_instance_details(instance_id=%(instance_id)s), When get instance detail occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            raise e
    def get_instance_details(self,instance_id):
        try:
            if instance_id:
                
                response_state, response_body = self.__get_instance_details(instance_id=instance_id)
                if response_state:
                    log.debug("METHOD: get_instance_details(instance_id=%(instance_id)s), get special instance detail success. response body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                    return (resultcode.Success, response_body)
                else:
                    log.warn("METHOD: get_instance_details(instance_id=%(instance_id)s), get special instance detail fail. response body: %(response_body)s." % {"instance_id": instance_id, "response_body": response_body})
                    return (resultcode.BadRequest, response_body)
        except Exception, e:
            log.error("METHOD: get_instance_details(instance_id=%(instance_id)s), When get instance detail occur an Exception: %(e)s." % {"instance_id": instance_id, "e": e})
            log.exception(e)
            raise e
            
    def __get_instance_busdetail(self, pinstance_detail):
        """
        get a special instance details include image, flavor, IPS and so on.
        {"server": {...}}
        """
        instance_data = pinstance_detail
        # pop server links
        instance_data["server"].pop("links")
        # pop image dict and put image_id
        if pinstance_detail["server"]["image"] != "":
            image_id = pinstance_detail["server"]["image"].get("id")
            instance_data["server"].pop("image")
            instance_data["server"]["image_id"] = image_id
        # pop flavro detail and get flavor detail
        flavor_id = instance_data["server"]["flavor"].get("id")
        flavor_o = flavors(tokens=self.tokens)
        return_state, return_body = flavor_o.get_flavor_by_id(flavor_id=flavor_id)
        if return_state:
            # success
            flavor1 = return_body
            # pop flavor links 
            flavor1["flavor"].pop("links")
            instance_data["server"].pop("flavor")
            instance_data["server"]["flavor"] = flavor1["flavor"]
            return instance_data
        else:
            # just return cpu/disk/ram information
            return instance_data
    
    def __create_instance(self, flavorRef, imageRef, name, uuid, port=None, adminPass=None, accessIPv4=None, fixed_ip=None, accessIPv6=None, security_group=None, user_data=None, availability_zone=None, metadata={}, personality=[]):
        """
        create instance and this instance will start from the special image 
        Creates a server.
        """
        try:
            # 1. 获取调用地址URL
            url = str(self.computer_endpoints["publicURL"] + "/servers")
            # 2. 构造request body
            request_body = openapi_param.get_create_instance_param(flavorRef=flavorRef, imageRef=imageRef, name=name, uuid=uuid, port=port, adminPass=adminPass, accessIPv4=accessIPv4, fixed_ip=fixed_ip, security_group=security_group, user_data=user_data, availability_zone=availability_zone, metadata=metadata, personality=personality, version=openapi_version.V2)
            # 3. 调用接口 
            return utils.postapi(url=url, par=request_body, token=self.tokenId)
        except Exception, e:
            log.error("METHOD:__create_instance(flavorRef=%(flavorRef)s, imageRef=%(imageRef)s, name=%(name)s, uuid=%(uuid)s, port=%(port)s, adminPass=%(adminPass)s, accessIPv4=%(accessIPv4)s, fixed_ip=%(fixed_ip)s, accessIPv6=%(accessIPv6)s, security_group=%(security_group)s, user_data=%(user_data)s, availability_zone=%(availability_zone)s, metadata=%(metadata)s, personality=%(personality)s), When create instance Occur an Exception: %(e)s." % {"flavorRef": flavorRef, "imageRef": imageRef, "name": name, "uuid": uuid, "port": port, "adminPass": adminPass, "accessIPv4": accessIPv4, "fixed_ip": fixed_ip, "accessIPv6": accessIPv6, "security_group": security_group, "user_data": user_data, "availability_zone": availability_zone, "metadata": metadata, "personality": personality, "e": e}), 
            log.exception(e)
            raise e
    
    def __create_instance_with_block_device_mapping(self, name, region, systen_volume_id, os_type, \
            imageRef, flavorRef, uuid, port=None, data_volume_id=None, security_group=None, user_data=None, availability_zone=None, \
            fixed_ip=None, metadata={}, personality=[], adminPass=None, delete_on_termination=True):
        """
        Creates a server with a block device mapping. 
        """
        try:
            # 1. build URL
            url = self.__get_compute_servers_url()
            # 2. build request body 
            request_boby = openapi_param.get_create_instance_with_block_device_mapping_param(name=name, adminPass=adminPass, \
                                systen_volume_id=systen_volume_id, os_type=os_type, data_volume_id=data_volume_id, imageRef=imageRef, flavorRef=flavorRef, \
                                uuid=uuid, port=port, security_group=security_group, user_data=user_data, availability_zone=availability_zone, \
                                fixed_ip=fixed_ip, metadata=metadata, personality=personality, delete_on_termination=delete_on_termination, version=openapi_version.V2)
            # 3. invoke OpenStack API to create instance with block device mapping
            response_state, response_body = utils.postapi(url=url, par=request_boby, token=self.tokenId)
            # judge create result 
            if response_state:
                # create success, pop links, return 
                log.debug("METHOD: __create_instance_with_block_device_mapping(**), create success.")
                return (True, response_body)
            else:
                # create fail, return response_body
                log.warn("METHOD: __create_instance_with_block_device_mapping(**), create fail. response_body: %(response_body)s." % {"response_body": response_body})
                return (False, response_body)
        except Exception, e:
            log.error("METHOD: __create_instance_with_block_device_mapping(**), When create instance Occur an Exception: %(e)s." % {"e": e})
            log.exception(e)
            raise e
    
    def __change_instance_password(self, instance_id, adminPass):
        """修改机器密码"""
        """Changes the password for a server. Specify the changePassword action in the request body."""
        try:
            # 1. 获取URL
            url = str(self.__get_compute_servers_url() + "/" + instance_id + "/action")
            # 2. 构造request body
            request_body = openapi_param.get_change_instance_password_parm(adminPass=adminPass)
            # 3. 调用接口，修改实例密码
            return utils.postapi(url=url, par=request_body, token=self.tokenId)
        except Exception, e:
            log.error('METHOD:__change_instance_password(instance_id="%(instance_id)s", adminPass="%(adminPass)s"), when changed instance password, occur an Exception: %(e)s.' % {"instance_id": instance_id, "adminPass": "******", "e": e})
            log.exception(e)
            raise e

    def attach_cdrom_to_instance_from_image(self,instance_id,imageRef):
        """
        attach_cdrom_to_instance_from_image(self,instance_id,imageRef):
        attach an cdrom from image to an instance 
        """    
        if not instance_id or not imageRef:
            log.info("Function  < attach_cdrom_to_instance_from_image >   raise  Exception  because  params : instanceid  or   imageRef  is None .")
            return (resultcode.InstanceOperateFailed,"instance id   imageref  is none .")
        log.info("ENTER  attach_cdrom_to_instance_from_image  with instance  %s  and  image %s "%(instance_id,imageRef))

        try:
            #判断被维护的云主机是否存在,不存在直接返回.
            return_state, return_body = self.__get_instance_details(instance_id)
            if not return_state:
                # not exist
                log.warn('METHOD: attach_cdrom_to_instance_from_image(instance_id=%(instance_id)s), The instance could not be found.' % {"instance_id": instance_id})
                return (resultcode.InstanceNotFound, None)
            
            #检查云主机是否已挂载，如果是则不允许挂载.
            check_before_attach = " select  count(*)   from  block_device_mapping  where  deleted_at  is null  and  device_type='cdrom'  and   disk_bus='ide'  and  instance_uuid = '%s' "%instance_id
            check_before_attach = db.execNovaSQL(check_before_attach)
            if check_before_attach[0][0] > 0:
                _msg = "Warn :  cannot  attch  any more  volumes  . Because  there exists  successful  attachment  already . if you  persisit  , Please try  to detach  first ."
                log.warn(_msg)
                return (resultcode.Success, {"success":"yes","msg":_msg})
            
            #1.根据工具img的imageref为其创建云硬盘.
            blockstorage_o = blockstorage(tokens=self.tokens)
            return_state, return_body = blockstorage_o.create_volume(size=40, availability_zone=None, source_volid=None, description="tool-volume", snapshot_id=None, name="tool-volume", imageRef=imageRef, volume_type=None, bootable=True, metadata=None)
            if not return_state and  "Success"  not  in str(return_body):
                return (resultcode.InstanceOperateFailed,"exception  happens when  creating  volume  for  tool  image . ")
            log.info("Creating  tool  volume  and  response :%s "%str(return_body)) 
            tool_volume_id = return_body["volumeId"]

            # 循环检查 新建的volume的状态  如果超时仍不可用就抛出异常;否则进入下一步;
            def _check_volume_status():
                return_state,return_body = blockstorage_o.get_volume_by_id(volume_id=tool_volume_id)
                if return_state and "available"  in str(return_body):
                    raise Exception("_check_volume_status : available volume . done .")
            _loop(f=_check_volume_status,maxtry=360,interval=10)
            log.info(" =====   post  volume  availablity  check . ===")
            
            #2.将新创的工具盘挂载到云主机上.
            status,response = self.attachment_volume_to_instance(instance_id, tool_volume_id)            
            if not status == resultcode.Success:
                log.info("Exception happens when attaching  tool-volume  %s  to  instance  %s"%(tool_volume_id,instance_id))
                return status,response
            log.info("Successfully  attach  tool-volume %s  to  instance  %s  . And response :  %s"%(tool_volume_id,instance_id,str(response)))  
            device = response["volumeAttachment"]["device"] 
            
            query_vdx = "select  connection_info  from  block_device_mapping  where  volume_id='%s'  and  instance_uuid = '%s'  and  deleted_at is   null "%(tool_volume_id,instance_id)
            #循环检查 新建volume的bdm状态 如果超时仍无 connection_info 则抛出异常;否则进入下一步
            def _check_bdm_status():
                findvdx_info = db.execNovaSQL(query_vdx)
                if "driver_volume_type"   in str(findvdx_info):
                    raise Exception("_check_bdm_state :  done .")                
            _loop(f=_check_bdm_status,maxtry=5,interval=5)
            #更新数据库 nova 的 block_device_mapping 
            update_cdrom = "update  block_device_mapping  set  device_type='cdrom'  ,  disk_bus='ide'  , boot_index=0  where  volume_id = '%s'"%tool_volume_id
            db.execNovaSQL(update_cdrom)            
            return (resultcode.Success, {"success":"yes"})
        except Exception, e:
            log.exception(e)
            raise e

    def delete_cdrom(self, instance_id):
        if not instance_id :
            log.info("Function  < delete_cdrom >   raise  Exception  because  params : instanceid    is None .")
            return (resultcode.InstanceOperateFailed,"instance id is none .")
        log.info("ENTER  delete_cdrom  with instance  %s  . "%instance_id)
        try:
            #判断被维护的云主机是否存在,不存在直接返回.
            return_state, return_body = self.__get_instance_details(instance_id)
            if not return_state:
                log.warn('METHOD: delete_cdrom(instance_id=%(instance_id)s), The instance could not be found.' % {"instance_id": instance_id})
                return (resultcode.InstanceNotFound, return_body)
            response_state,responsebody = self.list_volume_attachment_for_instance_inner(instance_id)
            if not response_state: #查询实例挂在的卷时发生异常
                _msg = "METHOD: delete_cdrom  raise Exception  while  querying  attachments  of  instance %s"%instance_id
                log.info(_msg)
                raise Exception(_msg)

            query_vdx = "select volume_id,id from block_device_mapping where deleted_at is null and device_type='cdrom' and disk_bus='ide' and boot_index=0 and instance_uuid='%s' "%instance_id 
            #查询数据库获取挂在系统盘的 volume_id
            query_vdx_result = db.execNovaSQL(query_vdx) 
            cdrom_uuid = query_vdx_result[0][0]
            cdrom_id =   query_vdx_result[0][1]
            update_cdrom = "update block_device_mapping set device_type=null,disk_bus=null,boot_index=null where id = '%s'"%cdrom_id
            db.execNovaSQL(update_cdrom) 
            #卸载工具盘
            return_state, return_body = self.delete_volume_from_instance_inner(instance_id=instance_id, attachment_id=cdrom_uuid)    # attachment_id  just same as  volume_id
            if not return_state:
                _msg = "Exception  happens while trying to  detach  tool volume  %s  from  instance  %s .  "%(cdrom_uuid,instance_id)
                log.info(_msg)
                raise Exception(_msg) 
            blockstorage_o = blockstorage(tokens=self.tokens)           
            def _check_detach_progress(): 
                return_state,return_body = blockstorage_o.describe_volume(cdrom_uuid)
                if return_state and "available"  in str(return_body):
                    raise Exception("Detachment  done . ") 
            #循环检查卸载 工具volume的进度，卸载完成则进入下一步- 删除.
            _loop(f=_check_detach_progress, maxtry=10, interval=3)

            #删除工具盘
            return_state, return_body = blockstorage_o.delete_volume(cdrom_uuid)
            if not  return_state:
                _msg = "Exception happens while removing  tool volume  %s from  instance  %s "%(cdrom_uuid,instance_id)
                log.exception(_msg)
                raise Exception(_msg)
            return (resultcode.Success, {"success":"yes"}) 
        except Exception, e:
            log.error('METHOD: delete_cdrom(instance_id=%(instance_id)s), when delete cdrom occur an exception: %(e)s' % {"instance_id": instance_id, "e": e})
            log.exception(e)
            return (resultcode.ServerError, e) 


    
class computer_agent(object):
    """
    computer对外提供的方法
    """
    __computer = None
    def __init__(self, tokens):
        """实例化computer"""
        self.__computer = computer(tokens=tokens)
    
    """instance manger"""
    def create_instance(self, hostname, region, image_id, cpu, ram, disk, bandwidth, network_name=None, uuid=None, adminPass=None, port=None, accessIPv4=None, fixed_ip=None, accessIPv6=None, security_group=None, user_data=None, availability_zone=None, metadata={}, personality=[]):
        """
        create a new instance
        uuid: network UUID,
        port: PORT 
        """
        return self.__computer.create_instance(hostname=hostname, adminPass=adminPass, region=region, image_id=image_id, cpu=cpu, ram=ram, disk=disk, bandwidth=bandwidth, network_name=network_name, uuid=uuid, port=port, accessIPv4=accessIPv4, fixed_ip=fixed_ip, accessIPv6=accessIPv6, security_group=security_group, user_data=user_data, availability_zone=availability_zone, metadata=metadata, personality=personality)
    
    def create_instance_with_block_device_mapping(self, name, region, systen_volume_id, image_id, cpu, ram, disk, bandwidth, network_name=None, uuid=None, port=None, os_type=1, data_volume_id=None, adminPass=None, security_group=None, user_data=None, availability_zone=None, fixed_ip=None, metadata={}, personality=[], delete_on_termination=True):
        """
        Creates a server with a block device mapping. 
        """
        return self.__computer.create_instance_with_block_device_mapping(name=name, adminPass=adminPass, region=region, systen_volume_id=systen_volume_id, data_volume_id=data_volume_id, image_id=image_id, os_type=os_type, cpu=cpu, ram=ram, disk=disk, bandwidth=bandwidth, network_name=network_name, uuid=uuid, port=port, security_group=security_group, user_data=user_data, availability_zone=availability_zone, fixed_ip=fixed_ip, metadata=metadata, personality=personality, delete_on_termination=delete_on_termination)
    
    def delete_instance(self, instance_id):
        """
        delete a special instance 
        """
        return self.__computer.delete_instance(instance_id=instance_id)
    
    def rebuild_instance(self, instance_id, imageRef, name, accessIPv4=None, accessIPv6=None, adminPass=None, metadata={}, personality=[]):
        """
        Rebuilds the specified server.
        """
        return self.__computer.rebuild_instance(instance_id=instance_id, imageRef=imageRef, name=name, adminPass=adminPass, accessIPv4=accessIPv4, accessIPv6=accessIPv6, metadata=metadata, personality=personality)
    
    def resize_instance(self, instance_id, cpu, ram, disk, bandwidth):
        """
        Resizes the specified server. Specify the resize action in the request body.
        """
        return self.__computer.resize_instance(instance_id=instance_id, cpu=cpu, ram=ram, disk=disk, bandwidth=bandwidth)
    
    def confirm_resize_instance(self, instance_id):
        """
        Confirms a pending resize action.
        """
        return self.__computer.confirm_resize_instance(instance_id=instance_id)
    
    def change_instance_password(self, instance_id, adminPass):
        """
        change instance password
        """
        return self.__computer.change_instance_password(instance_id=instance_id, adminPass=adminPass)
    
    """instance details"""
    # 获取指定用户下的全部实例 
    
    def describe_instance(self, instance_id):
        """
        get instance details
        """
        return self.__computer.describe_instance(instance_id=instance_id)
    
    def vnc_console(self, instance_id, vnc_type="novnc"):
        """
        Gets a console for a server instance.
        vnc_type: Valid values are novnc and xvpvnc. In now Environment the type of xvpvnc is unusable
        """
        return self.__computer.vnc_console(instance_id=instance_id, vnc_type=vnc_type)
    
    """instance power manager"""
    def start_instance(self, instance_id):
        """
        start an instance 
        """
        return self.__computer.start_instance(instance_id=instance_id)
    
    def stop_instance(self, instance_id):
        """关闭指定实例"""
        return self.__computer.stop_instance(instance_id=instance_id)
    
    def reboot_instance(self, instance_id, force=False):
        """重启指定实例"""
        if force:
            """hart reboot"""
            return self.__computer.hard_reboot_instance(instance_id=instance_id)
        else:
            """soft reboot"""
            return self.__computer.soft_reboot_instance(instance_id=instance_id)
    
    """manager instance volume"""
    def list_volume_attachment_for_instance(self, instance_id):
        """
        Lists the volume attachments for a specified server.
        """
        return self.__computer.list_volume_attachment_for_instance(instance_id=instance_id)
    
    def attachment_volume_to_instance(self, instance_id, volumeId):
        """attach the exits volume to the special instance"""
        return self.__computer.attachment_volume_to_instance(instance_id=instance_id, volumeId=volumeId)
    
    def delete_volume_from_instance(self, instance_id, attachment_id):
        """
        Deletes the specified volume attachment from a specified server.
        attachment_id: The id of the special volume which will delete from the special instance.
        """
        return self.__computer.delete_volume_from_instance(instance_id=instance_id, attachment_id=attachment_id)
    
    """IP manager"""
    def allocate_floating_ip_to_tenant(self, pool):
        """
        Allocates a new floating IP address to a tenant or account. 
        """
        return self.__computer.allocate_floating_ip(pool=pool)
    
    def deallocates_floating_ip_from_tenant(self, ip_id=None, address=None):
        """
        Deallocates the floating IP address associated with floating_IP_address_ID.
        """
        return self.__computer.deallocates_floating_ip(ip_id=ip_id, address=address)
    
    def add_floatingIp_to_instance(self, instance_id, address, fixed_address=None):
        """
        add a floating IP to the special instance 
        """
        return self.__computer.add_floatingIp_to_instance(instance_id=instance_id, address=address, fixed_address=fixed_address)
    
    def removes_floating_ip_from_instance(self, instance_id, address):
        """
        Removes a floating IP from an instance. 
        """
        return self.__computer.removes_floating_ip_from_instance(instance_id=instance_id, address=address)
    
    # 123 
    def list_os_floating_ips(self):
        """get floating IP"""
        return self.__computer.list_os_floating_ips()
    
#    def attachment_new_volume_to_instance(self, instance_id, size, description=None, name=None):
#        """向指定实例附加指定大小的volume"""
#        return self.__computer.attachment_new_volume_to_instance(instance_id=instance_id, size=size, description=description, name=name)
    #
    
    def create_security_group_rule(self, ip_protocol, from_port, to_port, cidr, security_group_id=None, name="default"):
        """
        Creates a security group rule 
        """
        return self.__computer.create_security_group_rule(security_group_id=security_group_id, name=name, ip_protocol=ip_protocol, from_port=from_port, to_port=to_port, cidr=cidr)
    
#    def deletes_security_group_rule(self):
#        """
#        Deletes a specified security group rule. 
#        """
        

    def attach_cdrom_to_instance_from_image(self,instance_id,imageRef):
        """
        attach an cdrom from image to an instance 
        """
        return self.__computer.attach_cdrom_to_instance_from_image(instance_id,imageRef)

    def delete_cdrom(self,instance_id):
        """
        delete cdrom from specified instance
        """
        return self.__computer.delete_cdrom(instance_id)

    def host_migration(self,origin_host,binary_name,dest_host,instance_list,is_close_coupute_node):
        """
        orgin_host:源主机
        dest_host:目标主机
        host migration计算节点上的虚拟机迁移
        """      
        return self.__computer.host_migration(origin_host=origin_host,binary_name=binary_name,dest_host=dest_host,instance_list=instance_list,is_close_coupute_node=is_close_coupute_node)
    
    #nova宿主机列表   
    def nova_hosts_list(self):
        """
        nova服务宿主机列表
        """      
        return self.__computer.nova_hosts_list()

    def instance_list_belong_to_specifed_service(self,host_name):
        """
        get specified service instance list
        """
        result_code,response_body = self.__computer.instance_list_belong_to_hypervisor(host_name=host_name)
        if result_code:
            return (resultcode.Success,response_body)
        else:
            return (resultcode.BadRequest,response_body)
    def get_instance_details(self,instance_id):
        """
        get specified instance details
        """
        return  self.__computer.get_instance_details(instance_id=instance_id)
        

    
