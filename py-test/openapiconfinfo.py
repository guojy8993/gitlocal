#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-02-21 10:30:25
# @Author  : l0uj1e (dajiesan@sohu.com)
# @Link    : http://sohu.com
# @Version : 1

class openapi_version(object):

    def __init__(self):
        pass

    V2 = "v2.0"

    V3 = "v3"


class openapi_param(object):

    def __init__(self):
        pass

    @staticmethod
    def get_auth_param(username, password, tenantId=None, tenantName=None, version=openapi_version.V2):
        """
        build auth parameter
        """
        if version == openapi_version.V3:
            pass
        else:
            if tenantName:
                return '{"auth":{"tenantName":"%(tenantName)s", "passwordCredentials":{"username":"%(username)s", "password":"%(password)s"}}}' % {"tenantName": tenantName, "username": username, "password": password}

            if tenantId:
                return '{"auth":{"tenantId":"%(tenantId)s", "passwordCredentials":{"username":"%(username)s", "password":"%(password)s"}}}' % {"tenantId": tenantId, "username": username, "password": password}

            return '{"auth":{"passwordCredentials":{"username":"%(username)s", "password":"%(password)s"}}}' % {"username": username, "password": password}
    
    """module flavors"""
    @staticmethod
    def get_create_flavors_parm(id, name, ram, vcpus, disk, version=openapi_version.V2):
        """
        build create new flavor parameter. 
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                        "flavor": {
                            "name": name,
                            "ram": ram,
                            "vcpus": vcpus,
                            "disk": disk,
                            "id": id,
                            "os-flavor-access:is_public": True
                        }
                    }
            return body
        
    @staticmethod
    def get_create_flavor_extra_specs_param(bandwidth, version=openapi_version.V2):
        """
        build create flavor extra-specs parameter.
        """
        import config
        if version == openapi_version.V3:
            pass
        else:
            inbound = config.FLAVOR_EXTRA_SPECS_KEY_INBOUND
            outbound = config.FLAVOR_EXTRA_SPECS_KEY_OUTBOUND
            body = {
                        "extra_specs": {
                            outbound: bandwidth
                        }
                    }
            if inbound is not None:
                body["extra_specs"]["inbound"] = bandwidth
            return body
    
    """module compute"""
    @staticmethod
    def get_create_instance_param(flavorRef, imageRef, name, uuid, port=None, adminPass=None, \
            accessIPv4=None, accessIPv6=None, security_group=None, user_data=None, fixed_ip=None, \
            availability_zone=None, metadata={}, personality=[], version=openapi_version.V2):
        """构造创建实例参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {"server": 
                   {
                        "name": name,
                        "imageRef": imageRef,
                        "metadata": metadata,
                        "personality": personality,
                        "flavorRef": flavorRef
                    }
                }
            if uuid:
                body["server"]["networks"] = [
                                              {
                                               "uuid": uuid,
                                               "port": port
                                               }]
            if adminPass: 
                body["server"]["adminPass"] = adminPass
            if accessIPv4:
                body["server"]["accessIPv4"] = accessIPv4
            if accessIPv6:
                body["server"]["accessIPv6"] = accessIPv6
            if security_group:
                body["server"]["security_group"] = security_group
            if user_data:
                body["server"]["user_data"] = user_data
            if availability_zone:
                body["server"]["availability_zone"] = availability_zone
            if fixed_ip:
                body["server"]["fixed_ip"] = fixed_ip
            return body
    
    @staticmethod
    def get_create_instance_with_block_device_mapping_param(name, adminPass, systen_volume_id, os_type, \
                data_volume_id, imageRef, flavorRef, uuid, port=None, security_group=None, \
                user_data=None, availability_zone=None, fixed_ip=None, metadata={}, personality=[], \
                delete_on_termination=True, version=openapi_version.V2):
        """
        get parameter Creates a server with a block device mapping. 
        """
        from commons import utils
        try:
            # 1. build use_data, which will contain password 
            if os_type == 0:
                # windows
                port = port if port is not None and port.isdigit() else "3389"
                passwd = \
                """rem cmd\r\nnet user administrator %(adminPass)s\r\nREG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal\" \"Server\\Wds\\rdpwd\\Tds\\tcp /v PortNumber /t REG_DWORD /d %(PortNumber)s /f \r\nREG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal\" \"Server\\WinStations\\RDP-Tcp /v PortNumber /t REG_DWORD /d  %(PortNumber)s /f \n""" % {"adminPass": adminPass,"PortNumber":port}
                user_data_pass = utils.base64Encode(s=passwd)
            elif os_type == 1:
                # ubuntu/centos 
                passwd = \
                """#!/bin/bash\n#modified vm's passwd\npasswd root <<EOF\n%(adminPass)s\n%(readminPass)s\nEOF""" % {"adminPass": adminPass, "readminPass": adminPass}
                user_data_pass = utils.base64Encode(s=passwd)
            # 2. built return paramter 
            if version == openapi_version.V3:
                pass
            else:
                if os_type == 1:
                # linux 
                    body = {
                            "server" : {
                                "name" : name,
                                "imageRef" : imageRef,
                                "flavorRef" : flavorRef,
                                "metadata" : {},
                                "personality" : personality,
                                "networks" : [
                                    {
                                        "uuid" : uuid
                                    }
                                ],
                                "block_device_mapping_v2": []
                            }
                        }
                if os_type == 0:
                # windows
                    body = {
                            "server" : {
                                "name" : name,
                                "imageRef" : imageRef,
                                "flavorRef" : flavorRef,
                                "metadata" : {"admin_pass":adminPass},
                                "personality" : personality,
                                "networks" : [
                                    {
                                        "uuid" : uuid
                                    }
                                ],
                                "block_device_mapping_v2": []
                            }
                        }
                #if port:
                #    body["server"]["networks"][0]["port"] = port
                if systen_volume_id:
                    # exist system volume
                    body["server"]["block_device_mapping_v2"].append({
                                                                        "device_name": "/dev/vda",
                                                                        "source_type": "volume",
                                                                        "destination_type": "volume",
                                                                        "delete_on_termination": delete_on_termination,
                                                                        "guest_format": None,
                                                                        "uuid": systen_volume_id,
                                                                        "boot_index": "0"
                                                                    })
                if data_volume_id:
                    body["server"]["block_device_mapping_v2"].append({
                                                                        "device_name": "/dev/sda",
                                                                        "source_type": "volume",
                                                                        "destination_type": "volume",
                                                                        "delete_on_termination": delete_on_termination,
                                                                        "guest_format": None,
                                                                        "uuid": data_volume_id,
                                                                        "boot_index": "1"
                                                                    })
                if security_group:
                    body["server"]["security_group"] = security_group
                if (user_data_pass or adminPass):
                    body["server"]["user_data"] = user_data_pass
                    body["server"]["config_drive"] = "true"
                if availability_zone:
                    body["server"]["availability_zone"] = availability_zone
                if fixed_ip: 
                    body["server"]["fixed_ip"] = fixed_ip
                if delete_on_termination:
                    body["server"]["delete_on_termination"] = delete_on_termination
                return body
        except Exception, e:
            raise e

    @staticmethod
    def get_change_instance_password_parm(adminPass, version=openapi_version.V2):
        """构造修改实例密码的参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "changePassword": {}
                }
            body["changePassword"]["adminPass"] = adminPass
            return body

    @staticmethod
    def get_resize_instance_inner_param(flavorRef, version=openapi_version.V2):
        """
        build resize instance parameter
        """
        if version ==openapi_version.V3:
            pass
        else:
            body = {
                    "resize" : {
                        "flavorRef" : flavorRef
                    }
                }
            return body

    @staticmethod
    def get_confirm_resize_instance_inner_param(version=openapi_version.V2):
        """
        get confirm resize instance parameter
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "confirmResize" : None
                }
            return body;

    @staticmethod
    def get_rebuild_instance_param(imageRef, name, adminPass, accessIPv4, accessIPv6, metadata, personality, version=openapi_version.V2):
        """
        get rebuild instance parameter
        "metadata" : {
            "meta var" : "meta val"
        }
        "personality" : [
            {
                "path" : "/etc/banner.txt",
                "contents" : "ICAgICAgDQoiQSBjbG91ZCBkb2VzIG5vdCBrbm93IHdoeSBp dCBtb3ZlcyBpbiBqdXN0IHN1Y2ggYSBkaXJlY3Rpb24gYW5k IGF0IHN1Y2ggYSBzcGVlZC4uLkl0IGZlZWxzIGFuIGltcHVs c2lvbi4uLnRoaXMgaXMgdGhlIHBsYWNlIHRvIGdvIG5vdy4g QnV0IHRoZSBza3kga25vd3MgdGhlIHJlYXNvbnMgYW5kIHRo ZSBwYXR0ZXJucyBiZWhpbmQgYWxsIGNsb3VkcywgYW5kIHlv dSB3aWxsIGtub3csIHRvbywgd2hlbiB5b3UgbGlmdCB5b3Vy c2VsZiBoaWdoIGVub3VnaCB0byBzZWUgYmV5b25kIGhvcml6 b25zLiINCg0KLVJpY2hhcmQgQmFjaA=="
            }
        ]
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "rebuild" : {
                        "imageRef" : imageRef,
                        "name" : name,
                        "metadata" : metadata,
                        "personality" : personality
                    }
                }
            if accessIPv4:
                body["rebuild"]["accessIPv4"] = accessIPv4
            if accessIPv6:
                body["rebuild"]["accessIPv6"] = accessIPv6
            if adminPass:
                body["rebuild"]["adminPass"] = adminPass
            return body

    @staticmethod
    def get_add_floatingIp_to_instance_param(address, fixed_address = None, version=openapi_version.V2):
        """构造为实例添加floating IP 参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
               "addFloatingIp":{
                  "address": address
               }
            }
            if fixed_address is not None:
                body["addFloatingIp"]["fixed_address"] = fixed_address
            return body
            
    @staticmethod
    def get_allocate_floating_ip_parm(pool, version=openapi_version.V2):
        """构造从IP池分配ip方法的参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "pool": pool
                }
            return body
    
    @staticmethod
    def get_removes_a_floating_ip_param(address, version=openapi_version.V2):
        """构造移除浮动IP方法的参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "removeFloatingIp": {
                        "address": address
                    }
                }
            return body
    
    @staticmethod
    def get_attachment_volume_to_instance_inner_parm(volumeId, deviceType="NT", version=openapi_version.V2):
        """构造attachment volume to instance的parm"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "volumeAttachment": {
                        "volumeId": volumeId,
                        "OS-DCF:diskConfig": "AUTO"
                    }
                }
            if deviceType == "NT":
                body["volumeAttachment"]["device"] = None
            else:
                body["volumeAttachment"]["device"] = "auto"
            return body
    
    @staticmethod
    def get_vnc_console_parm(vnc_type, version=openapi_version.V2):
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "os-getVNCConsole": {
                        "type": vnc_type
                    }
                }
            return body
    
    @staticmethod
    def get_create_security_group_rule_inner_param(group_id, parent_group_id, ip_protocol, from_port, to_port, cidr, version=openapi_version.V2):
        """
        create security group rule parameter 
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                        "security_group_rule": {
                            "ip_protocol": ip_protocol,
                            "from_port": from_port,
                            "to_port": to_port,
                            "cidr": cidr,
                            "group_id": None,
                            "parent_group_id": parent_group_id
                        }
                    }
            return body        
    
    @staticmethod
    def get_updates_nova_quotas_inner_param(cores, fixed_ips, floating_ips, injected_file_content_bytes, injected_file_path_bytes, injected_files, instances, key_pairs, metadata_items, ram, security_group_rules, security_groups, version=openapi_version.V2):
        """
        build updates nova quotas parameter. 
        """
        if version==openapi_version.V3:
            pass
        else:
            body = {
                        "quota_set": {
                            "cores": cores,
                            "fixed_ips": fixed_ips,
                            "floating_ips": floating_ips,
                            "injected_file_content_bytes": injected_file_content_bytes,
                            "injected_file_path_bytes": injected_file_path_bytes,
                            "injected_files": injected_files,
                            "instances": instances,
                            "key_pairs": key_pairs,
                            "metadata_items": metadata_items,
                            "ram": ram,
                            "security_group_rules": security_group_rules,
                            "security_groups": security_groups
                        }
                    }
            return body 
    
    """module block storage的构造参数的方法"""
    @staticmethod
    def get_creates_volume_parm(size, availability_zone=None, source_volid=None, description=None, snapshot_id=None, \
            name=None, imageRef=None, volume_type=None, bootable=None, metadata=None, version=openapi_version.V2):
        """构造创建VOLUME的方法"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                   "volume":{
                        "size": size
                    }
                }
            if availability_zone:
                body["volume"]["availability_zone"] = availability_zone
                
            if imageRef:
                body["volume"]["imageRef"] = imageRef
            elif source_volid:
                body["volume"]["source_volid"] = source_volid
            elif snapshot_id:
                body["volume"]["snapshot_id"] = snapshot_id
                
            if description:
                body["volume"]["description"] = description
            if name:
                body["volume"]["name"] = name
            if volume_type:
                body["volume"]["volume_type"] = volume_type
            if bootable:
                body["volume"]["bootable"] = bootable
            if metadata:
                body["volume"]["metadata"] = metadata
            return body
    
    @staticmethod
    def get_update_volume_parm(name=None, description=None, version=openapi_version.V2):
        """构造更新volume的方法"""
        if version == openapi_version.V3:
            pass
        else:
            body = {"volume": {}}
            if name:
                body["volume"]["name"] = name
            if description:
                body["volume"]["description"] = description
            return body
    
    @staticmethod
    def get_create_snapshot_parm(instance_id, volume_id, force=True, name=None, description=None, version=openapi_version.V2):
        """构造创建快照的参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "snapshot": {
                        "volume_id": volume_id,
                        "force": force
                     }
                }
            if name is not None:
                body["snapshot"]["name"] = name
            if description is not None:
                body["snapshot"]["description"] = description
            return body
    
    @staticmethod
    def get_create_backup_parm(volume_id,container,name,description=None,version=openapi_version.V2):
        """构造创建备份的参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "backup": {
                           "volume_id": volume_id,
                           "container": container,
                           "name": name
                            }
                    }
            if description is not None:
                body["backup"]["description"] = description
            return body
   
    @staticmethod
    def get_restore_backup_parm(backup_id,volume_id,version=openapi_version.V2):
        """构造还原备份的参数"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "restore": {
                           "backup_id": backup_id,
                           "volume_id": volume_id
                            }
                    }
            return body 
    
    """module identity构造参数的方法"""
    @staticmethod
    def get_create_tenant_inner_parm(name, description=None, enabled=False, version=openapi_version.V2):
        """build create tenant parmeter"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "tenant": 
                    {
                     "name": name, 
                     "enabled": bool(enabled)
                     }
                }
            if description is not None:
                body["tenant"]["description"] = description
            return body
    
    @staticmethod
    def get_create_user_inner_parm(name, password, enabled, email, domain_id, default_project_id, description, version=openapi_version.V3):
        """get create user parmeter"""
        if version == openapi_version.V3:
            body = {
                    "user": 
                    {
                     "name": name, 
                     "password": password, 
                     "enabled": enabled, 
                     "email": email, 
                     "domain_id": domain_id, 
                     "default_project_id": default_project_id, 
                     "description": description
                     }
                }
            return body
        else:
            pass
    
    """module networking"""
    @staticmethod
    def get_create_network_param(name=None, tenant_id=None, admin_state_up=None, shared=None, version=openapi_version.V2):
        """built create network parameter"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                       "network":{
                       }
                    }
            if name is not None:
                body["network"]["name"] = name
            if tenant_id is not None:
                body["network"]["tenant_id"] = tenant_id
            if admin_state_up is not None:
                body["network"]["admin_state_up"] = admin_state_up
            if shared is not None:
                body["network"]["shared"] = shared
            return body
			
    @staticmethod
    def get_update_port_param(port_id=None,port_admin=None,version=openapi_version.V2):
        """build update port admin state parameter"""
        if version == openapi_version.V3:
            pass
        else:
            body = {"port":{}}
            body["id"]=port_id
            body["port"]["admin_state_up"]=port_admin
            return body
	
    @staticmethod
    def get_create_subnet_param(name, network_id, tenant_id, allocation_pools, gateway_ip, cidr, enable_dhcp, dns_nameservers=None, preferred_DNS=None, alternate_DNS=None, ip_version=4, version=openapi_version.V2):
        """built create subnet parameter"""
        if version == openapi_version.V3:
            pass
        else:
            body = {
                        "subnet":{
                            "network_id": network_id,
                            "ip_version": ip_version,
                            "cidr": cidr
                       }
                    }
            if name:
                body["subnet"]["name"] = name
            if tenant_id:
                body["subnet"]["tenant_id"] = tenant_id
            if allocation_pools:
                body["subnet"]["allocation_pools"] = allocation_pools
            if gateway_ip:
                body["subnet"]["gateway_ip"] = gateway_ip
            if enable_dhcp: 
                body["subnet"]["enable_dhcp"] = enable_dhcp
            if dns_nameservers:
                body["subnet"]["dns_nameservers"]=[]
            if preferred_DNS:
                body["subnet"]["dns_nameservers"].append(preferred_DNS)
            if alternate_DNS:
                body["subnet"]["dns_nameservers"].append(alternate_DNS)
            return body
    
    @staticmethod
    def get_updates_quotas_inner_param(security_group, security_group_rule, network, subnet, router, port, floatingip, version=openapi_version.V2):
        """
        build updates quotas 
        """
        if version==openapi_version.V3:
            pass
        else:
            body = {
                        "quota": {
                            "subnet": subnet,
                            "network": network,
                            "floatingip": floatingip,
                            "security_group_rule": security_group_rule,
                            "security_group": security_group,
                            "router": router,
                            "port": port
                        }
                    }
            return body 
    
    """routers"""
    @staticmethod
    def get_create_routers(name, admin_state_up, external_network_id, version=openapi_version.V2):
        """
        build create new routers parameter
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                       "router":{
                          "name": name,
                          "admin_state_up": admin_state_up,
                          "external_gateway_info" :
                            {
                              "network_id": external_network_id
                            }
                       }
                    }
            return body
    
    @staticmethod
    def get_add_router_interface_param(subnet_id=None, port_id=None, version=openapi_version.V2):
        """
        build add router interface parameter to add ...
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {}
            if subnet_id:
                body["subnet_id"] = subnet_id
            else:
                body["port_id"] = port_id
            return body 
    
    @staticmethod
    def get_remove_router_interface_param(subnet_id, port_id, version=openapi_version.V2):
        """
        build remove router interface param
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {}
            if subnet_id:
                body["subnet_id"] = subnet_id
            else:
                body["port_id"] = port_id
            return body
	
    @staticmethod
    def get_remove_router_interface_param(subnet_id, port_id, version=openapi_version.V2):
        """
        build remove router interface param
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {}
            if subnet_id:
                body["subnet_id"] = subnet_id
            else:
                body["port_id"] = port_id
            return body
    
    @staticmethod
    def get_updates_disable_host_service_param(host_name,binary_name, version=openapi_version.V2):
        """
        build disable host service interface param
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                    "host":host_name,
                    "binary":binary_name 
                    }
            return body
    
    @staticmethod
    def get_updates_hot_live_migration_param(host=None,block_migration=False,disk_over_commit=False, version=openapi_version.V2):
        """
        build hot live migration interface param
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                        "os-migrateLive": {
                            "host": host,
                            "block_migration":block_migration,
                            "disk_over_commit":disk_over_commit
                                        
                        }
                    }
            return body
    
    @staticmethod
    def get_updates_cold_live_migration_param(version=openapi_version.V2):
        """
        build cold live migration interface param
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                        "migrate":None
                    }
            return body
    
    @staticmethod
    def get_attach_cdrom_to_instance_from_image_param(instance_id,imageRef,version=openapi_version.V2):
       
        if version == openapi_version.V3:
            pass
        else:
            body = {
                       "cdrom-attach":{
                          "image_id": imageRef
                       }
                    }
        return body

    @staticmethod
    def get_detach_cdrom_to_instance_from_image_param(version=openapi_version.V2):
        """
        build detach cdrom to instance params
        """
        if version == openapi_version.V3:
            pass
        else:
            body = {
                       "cdrom-detach":"null"
                    }
        return body
    @staticmethod
    def get_quota_vol_update_params(volumes,snapshots,gigabytes,version=openapi_version.V2):
        if version == openapi_version.V3:
            pass
        else:
            print "METHOD: get_quota_vol_update_params"
            body = {
                           "quota_set": {
                                            "volumes":volumes,
                                            "snapshots":snapshots,
                                            "gigabytes":gigabytes
                                          }
                    }
        return body 
    
class openapi_url(object):

    def __init__(self):
        pass

    @staticmethod
    def get_auth_url(version=openapi_version.V2):
        if version == openapi_version.V3:
            return "/%s/auth/tokens" % openapi_version.V3
        else:
            return "/%s/tokens" % openapi_version.V2

class openapi_endpoint_type(object):

    def __init__(self):
        pass

    COMPUTER = "compute"
    
    NOVA = "nova"

    NETWORK = "network"

    IMAGE = "image"

    VOLUME = "volume"
    
    VOLUMEV2 = "volumev2"

    IDENTITY = "identity"

    OBJECTSTORE = "object-store"

    EC2 = "ec2"

    METERING = "metering"

    S3 = "s3"
