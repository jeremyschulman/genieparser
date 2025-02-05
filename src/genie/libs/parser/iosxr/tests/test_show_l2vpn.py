# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device
from ats.topology import loader

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

# iosxr show_mrib
from genie.libs.parser.iosxr.show_l2vpn import (ShowL2vpnMacLearning,
                                                ShowL2vpnBridgeDomain,
                                                ShowL2vpnForwardingBridgeDomainMacAddress,
                                                ShowL2vpnForwardingProtectionMainInterface,
                                                ShowL2vpnBridgeDomainSummary,
                                                ShowL2vpnBridgeDomainBrief,
                                                ShowL2vpnBridgeDomainDetail)
# ===========================================
# Unit test for 'show l2vpn mac-learning {mac_type} all location {location}'
# ===========================================
class TestShowL2vpnMacLearning(unittest.TestCase):
    """Unit test for 'show l2vpn mac-learning <mac_type> all location <location>'"""

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    expected_output = {
        'topo_id': {
            '1': {
                'producer': {
                    '0/0/CPU0': {
                        'next_hop': {
                            'BE1.7': {
                                'mac_address': {
                                    '7777.7777.0002': {
                                        'ip_address': []}}}}}}},
            '6': {
                'producer': {
                    '0/0/CPU0': {
                        'next_hop': {
                            'BV1': {
                                'mac_address': {
                                    '0000.f65a.357c': {
                                        'ip_address': ['fe80::200:f6ff:fe5a:357c']},
                                    '1000.0001.0001': {
                                        'ip_address': ['10.1.1.11']}}}}}}},
            '7': {
                'producer': {
                    '0/0/CPU0': {
                        'next_hop': {
                            'BV2': {
                                'mac_address': {
                                    '0000.f65a.3570': {
                                        'ip_address': [
                                            '10.1.2.91', '10.1.2.93']}}}}}}}}}

    device_output = {'execute.return_value': '''
        Topo ID  Producer  Next Hop(s)  Mac Address     IP Address

        6        0/0/CPU0   BV1        1000.0001.0001      10.1.1.11
        7        0/0/CPU0   BV2        0000.f65a.3570      10.1.2.91
        7        0/0/CPU0   BV2        0000.f65a.3570      10.1.2.93
        1        0/0/CPU0   BE1.7      7777.7777.0002
        6        0/0/CPU0   BV1        0000.f65a.357c      fe80::200:f6ff:fe5a:357c

    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnMacLearning(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.device_output)
        obj = ShowL2vpnMacLearning(device=self.device)
        parsed_output = obj.parse()

        self.assertEqual(parsed_output, self.expected_output)


# ===========================================
#  Unit test for 'show l2vpn bridge-domain'
# ===========================================

class TestShowL2vpnBridgeDomain(unittest.TestCase):
    '''Unit test for "show l2vpn bridge-domain"'''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'bridge_group': {
            'g1': {
                'bridge_domain': {
                    'EVPN-Multicast-BTV': {
                        'id': 0,
                        'state': 'up',
                        'shg_id': 0,
                        'mst_i': 0,
                        'mac_aging_time': 300,
                        'mac_limit': 4000,
                        'mac_limit_action': 'none',
                        'mac_limit_notification': 'syslog',
                        'filter_mac_address': 0,
                        'ac': {
                            'num_ac': 1,
                            'num_ac_up': 1,
                            'interfaces': {
                                'GigabitEthernet0/1/0/0': {
                                    'state': 'up',
                                    'static_mac_address': 2,
                                    'mst_i': 0,
                                    'mst_i_state': 'unprotected',
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 1,
                            1: {
                                'neighbor': {
                                    '10.1.1.1': {
                                        'pw_id': {
                                            1: {
                                                'state': 'up',
                                                'static_mac_address': 0,
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        'pw': {
                            'num_pw': 1,
                            'num_pw_up': 1,
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        RP/0/RP0/CPU0:router# show l2vpn bridge-domain

        Bridge group: g1, bridge-domain: EVPN-Multicast-BTV, id: 0, state: up, ShgId: 0, MSTi: 0
          Aging: 300 s, MAC limit: 4000, Action: none, Notification: syslog
          Filter MAC addresses: 0
          ACs: 1 (1 up), VFIs: 1, PWs: 1 (1 up)
          List of ACs:
            Gi0/1/0/0, state: up, Static MAC addresses: 2, MSTi: 0 (unprotected)
          List of Access PWs:
          List of VFIs:
            VFI 1
              Neighbor 10.1.1.1 pw-id 1, state: up, Static MAC addresses: 0
    '''}

    golden_parsed_output2 = {
        'bridge_group': {
            'EVPN-Mulicast': {
                'bridge_domain': {
                    'EVPN-Multicast-BTV': {
                        'id': 0,
                        'state': 'up',
                        'shg_id': 0,
                        'mst_i': 0,
                        'mac_aging_time': 300,
                        'mac_limit': 4000,
                        'mac_limit_action': 'none',
                        'mac_limit_notification': 'syslog',
                        'filter_mac_address': 0,
                        'ac': {
                            'num_ac': 3,
                            'num_ac_up': 2,
                            'interfaces': {
                                'BV100': {
                                    'state': 'up',
                                    'bvi_mac_address': 1,
                                },
                                'Bundle-Ether3.100': {
                                    'state': 'down',
                                    'static_mac_address': 0,
                                    'mst_i': 5,
                                },
                                'Bundle-Ether4.100': {
                                    'state': 'up',
                                    'static_mac_address': 0,
                                    'mst_i': 5,
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 0,
                        },
                        'pw': {
                            'num_pw': 0,
                            'num_pw_up': 0,
                        },
                        'pbb': {
                            'num_pbb': 0,
                            'num_pbb_up': 0,
                        },
                        'vni': {
                            'num_vni': 0,
                            'num_vni_up': 0,
                        },
                        'evpn': {
                            'EVPN': {
                                'state': 'up',
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
        show l2vpn bridge-domain

        Mon Oct  7 16:18:58.402 EDT
        Legend: pp = Partially Programmed.
        Bridge group: EVPN-Mulicast, bridge-domain: EVPN-Multicast-BTV, id: 0, state: up, ShgId: 0, MSTi: 0
        Aging: 300 s, MAC limit: 4000, Action: none, Notification: syslog
        Filter MAC addresses: 0
        ACs: 3 (2 up), VFIs: 0, PWs: 0 (0 up), PBBs: 0 (0 up), VNIs: 0 (0 up)
        List of EVPNs:
            EVPN, state: up
        List of ACs:
            BV100, state: up, BVI MAC addresses: 1
            BE3.100, state: down, Static MAC addresses: 0, MSTi: 5
            BE4.100, state: up, Static MAC addresses: 0, MSTi: 5
        List of Access PWs:
        List of VFIs:
        List of Access VFIs:
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnBridgeDomain(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowL2vpnBridgeDomain(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowL2vpnBridgeDomain(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output2)

# ====================================================================================
#  Unit test for 'show l2vpn forwarding bridge-domain mac-address location {location}'
# ====================================================================================
class TestShowL2vpnForwardingBridgeDomain(unittest.TestCase):
    '''Unit test for
        show l2vpn forwarding bridge-domain mac-address location {location}
        show l2vpn forwarding bridge-domain {bridge_domain} mac-address location {location}
    '''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'mac_table': {
            'Te0/0/1/0/3.3': {
                'mac_address': {
                    '0001.0000.0002': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0003': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0004': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0005': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0006': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0007': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0008': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0009': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                     '0001.0000.000a': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.000b': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.000c': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.000d': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.000e': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.000f': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0010': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0011': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0012': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'},
                    '0001.0000.0013': {
                        'lc_learned': 'N/A',
                        'learned_from': 'Te0/0/1/0/3.3',
                        'mapped_to': 'N/A',
                        'resync_age': '0d '
                                      '0h '
                                      '0m '
                                      '14s',
                        'type': 'dynamic'}
                }
            }
        }
    }

    golden_output = {'execute.return_value': '''
        RP/0/RP0/CPU0:ios#show l2vpn forwarding bridge-domain mac-address location 0/$
        Wed Jul 3 14:10:20.666 UTC
        To Resynchronize MAC table from the Network Processors, use the command...
        l2vpn resynchronize forwarding mac-address-table location <r/s/i>

        Mac Address Type Learned from/Filtered on LC learned Resync Age/Last Change Mapped to 
        -------------- ------- --------------------------- ---------- ---------------------- -------------- 
        0001.0000.0002 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0003 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0004 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0005 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0006 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0007 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0008 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0009 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.000a dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.000b dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.000c dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.000d dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.000e dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.000f dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0010 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0011 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0012 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A 
        0001.0000.0013 dynamic Te0/0/1/0/3.3 N/A 0d 0h 0m 14s N/A
    '''}

    golden_parsed_output_1 = {
        'mac_table': {
            '(10.25.40.40, 10007)': {
                'mac_address': {
                    '0021.0001.0002': {
                        'lc_learned': 'N/A',
                        'learned_from': '(10.25.40.40, '
                                       '10007)',
                        'mapped_to': 'N/A',
                        'resync_age': '14 '
                                     'Mar '
                                     '12:46:04',
                        'type': 'dynamic'},
                    '1234.0001.0005': {'lc_learned': 'N/A',
                        'learned_from': '(10.25.40.40, '
                                       '10007)',
                        'mapped_to': 'N/A',
                        'resync_age': 'N/A',
                        'type': 'static'}
                }
            },
            'BD id:0': {
                'mac_address': {
                    '0021.0001.0001': {
                        'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '0021.0001.0003': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '0021.0001.0004': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '0021.0001.0005': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '1234.0001.0001': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '1234.0001.0002': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '1234.0001.0003': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'},
                    '1234.0001.0004': {'lc_learned': 'N/A',
                                      'learned_from': 'BD '
                                                      'id:0',
                                      'mapped_to': 'N/A',
                                      'resync_age': 'N/A',
                                      'type': 'EVPN'}
                }
            },
            'BE1.2': {
                'mac_address': {
                    '0021.0002.0005': {
                        'lc_learned': 'N/A',
                        'learned_from': 'BE1.2',
                        'mapped_to': 'N/A',
                        'resync_age': '14 '
                                      'Mar '
                                      '12:46:04',
                        'type': 'dynamic'},
                    '1234.0002.0004': {
                        'lc_learned': 'N/A',
                        'learned_from': 'BE1.2',
                        'mapped_to': 'N/A',
                        'resync_age': 'N/A',
                        'type': 'static'}
                }
            }
        }
    }

    golden_output_1 = {'execute.return_value': '''
        RP/0/RP0/CPU0:router# show l2vpn forwarding bridge-domain mac-address location 0
        Mac Address    Type    Learned from/Filtered on    LC learned Resync Age/Last Change Mapped to
        -------------- ------- --------------------------- ---------- ---------------------- --------------
        0021.0001.0001 EVPN    BD id: 0                    N/A        N/A                    N/A
        0021.0001.0003 EVPN    BD id: 0                    N/A        N/A                    N/A
        0021.0001.0004 EVPN    BD id: 0                    N/A        N/A                    N/A
        0021.0001.0005 EVPN    BD id: 0                    N/A        N/A                    N/A
        1234.0001.0001 EVPN    BD id: 0                    N/A        N/A                    N/A
        1234.0001.0002 EVPN    BD id: 0                    N/A        N/A                    N/A
        1234.0001.0003 EVPN    BD id: 0                    N/A        N/A                    N/A
        1234.0001.0004 EVPN    BD id: 0                    N/A        N/A                    N/A
        0021.0001.0002 dynamic (10.25.40.40, 10007)        N/A        14 Mar 12:46:04        N/A
        1234.0001.0005 static  (10.25.40.40, 10007)        N/A        N/A                    N/A
        0021.0002.0005 dynamic BE1.2                       N/A        14 Mar 12:46:04        N/A
        1234.0002.0004 static  BE1.2                       N/A        N/A                    N/A
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnForwardingBridgeDomainMacAddress(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(location=0)

    def test_missing_attribute(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnForwardingBridgeDomainMacAddress(device=self.device)
        with self.assertRaises(TypeError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnForwardingBridgeDomainMacAddress(device=self.device)
        parsed_output = obj.parse(location=0)
        self.assertEqual(parsed_output, self.golden_parsed_output)

    def test_golden_1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_1)
        obj = ShowL2vpnForwardingBridgeDomainMacAddress(device=self.device)
        parsed_output = obj.parse(location=0, bridge_domain=0)
        self.assertEqual(parsed_output, self.golden_parsed_output_1)

# ====================================================================================
#  Unit test for 'show l2vpn forwarding protection main-interface location {location}'
# ====================================================================================
class TestShowL2vpnForwardingProtectionMainInterface(unittest.TestCase):
    '''Unit test for
        show l2vpn forwarding protection main-interface location {location}
    '''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'main_interface_id': {
            'GigabitEthernet0/0/0/0': {
                'instance': {
                    '1': {
                        'state': 'forward'},
                    '2': {
                        'state': 'forward'}
                }
            },
            'GigabitEthernet0/0/0/1': {
                'instance': {
                    '1': {
                        'state': 'forward'}
                }
            }
        }
    }

    golden_output = {'execute.return_value': '''
        RP/0/RP0/CPU0:router# show l2vpn forwarding protection main-interface location 0/1/0
        Main Interface ID                Instance    State    
        -------------------------------- -------------- -------- 
        GigabitEthernet0/0/0/0           1               forward       
        GigabitEthernet0/0/0/0           2               forward                
        GigabitEthernet0/0/0/1           1               forward  
    '''}

    golden_parsed_output_1 = {
        'main_interface_id': {
            'PW:10.25.40.40,10001': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'BLOCKED'}
                }
            },
            'PW:10.25.40.40,10007': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'FORWARDING'}
                }
            },
            'PW:10.25.40.40,10011': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'FORWARDING'}
                }
            },
            'PW:10.25.40.40,10017': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'}
                }
            },
            'VFI:ves-vfi-1': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'BLOCKED'}
                }
            },
            'VFI:ves-vfi-2': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'FORWARDING'}
                }
            },
            'VFI:ves-vfi-3': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'BLOCKED'}
                }
            },
            'VFI:ves-vfi-4': {
                'instance': {
                    '0': {
                        'state': 'FORWARDING'},
                    '1': {
                        'state': 'FORWARDING'}
                }
            }
        }
    }

    golden_output_1 = {'execute.return_value': '''
        RP/0/RP0/CPU0:router# show l2vpn forwarding protection main-interface location 0/2/1
        Main Interface ID                Instance   State
        -------------------------------- ---------- ------------
        VFI:ves-vfi-1                    0          FORWARDING
        VFI:ves-vfi-1                    1          BLOCKED
        VFI:ves-vfi-2                    0          FORWARDING
        VFI:ves-vfi-2                    1          FORWARDING
        VFI:ves-vfi-3                    0          FORWARDING
        VFI:ves-vfi-3                    1          BLOCKED
        VFI:ves-vfi-4                    0          FORWARDING
        VFI:ves-vfi-4                    1          FORWARDING
        PW:10.25.40.40,10001             0          FORWARDING
        PW:10.25.40.40,10001             1          BLOCKED
        PW:10.25.40.40,10007             0          FORWARDING
        PW:10.25.40.40,10007             1          FORWARDING
        PW:10.25.40.40,10011             0          FORWARDING
        PW:10.25.40.40,10011             1          FORWARDING
        PW:10.25.40.40,10017             0          FORWARDING
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnForwardingProtectionMainInterface(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(location='0/1/0')

    def test_missing_argument(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnForwardingProtectionMainInterface(device=self.device)
        with self.assertRaises(TypeError):
            parsed_output = obj.parse()

# ==================================================
#  Unit test for 'show l2vpn bridge-domain summary'
# ==================================================

class TestShowL2vpnBridgeDomainSummary(unittest.TestCase):
    '''Unit test for "show l2vpn bridge-domain summary"'''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'number_of_groups': 1,
        'bridge_domains': {
            'total': 1,
            'up': 1,
            'shutdown': 0,
        },
        'ac': {
            'total': 1,
            'up': 1,
            'down': 0,
        },
        'pw': {
            'total': 1,
            'up': 1,
            'down': 0,
        },
    }

    golden_output1 = {'execute.return_value': '''
        Device1# show l2vpn bridge-domain summary

        Number of groups: 1, bridge-domains: 1, Up: 1, Shutdown: 0
        Number of ACs: 1 Up: 1, Down: 0
        Number of PWs: 1 Up: 1, Down: 0
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnBridgeDomainSummary(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowL2vpnBridgeDomainSummary(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)

# ==================================================
#  Unit test for 'show l2vpn bridge-domain summary'
# ==================================================

class TestShowL2vpnBridgeDomainBrief(unittest.TestCase):
    '''Unit test for "show l2vpn bridge-domain summary"'''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'bridge_group': {
            'g1': {
                'bridge_domain': {
                    'bd1': {
                        'id': 0,
                        'state': 'up',
                        'ac': {
                            'num_ac': 1,
                            'num_ac_up': 1,
                        },
                        'pw': {
                            'num_pw': 1,
                            'num_pw_up': 1,
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        Device1# show l2vpn bridge-domain brief

        Bridge Group/Bridge-Domain Name  ID    State      Num ACs/up     Num PWs/up
        -------------------------------- ----- ---------- -------------- --------------
        g1/bd1                           0     up         1/1            1/1 
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnBridgeDomainBrief(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowL2vpnBridgeDomainBrief(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)
        
# ==================================================
#  Unit test for 'show l2vpn bridge-domain summary'
# ==================================================

class TestShowL2vpnBridgeDomainSummary(unittest.TestCase):
    '''Unit test for "show l2vpn bridge-domain summary"'''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'number_of_groups': 1,
        'bridge_domains': {
            'total': 1,
            'up': 1,
            'shutdown': 0,
        },
        'ac': {
            'total': 1,
            'up': 1,
            'down': 0,
        },
        'pw': {
            'total': 1,
            'up': 1,
            'down': 0,
        },
    }

    golden_output1 = {'execute.return_value': '''
        Device1# show l2vpn bridge-domain summary

        Number of groups: 1, bridge-domains: 1, Up: 1, Shutdown: 0
        Number of ACs: 1 Up: 1, Down: 0
        Number of PWs: 1 Up: 1, Down: 0
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnBridgeDomainSummary(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowL2vpnBridgeDomainSummary(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)

# ==================================================
#  Unit test for 'show l2vpn bridge-domain summary'
# ==================================================

class TestShowL2vpnBridgeDomainBrief(unittest.TestCase):
    '''Unit test for "show l2vpn bridge-domain summary"'''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'bridge_group': {
            'g1': {
                'bridge_domain': {
                    'bd1': {
                        'id': 0,
                        'state': 'up',
                        'ac': {
                            'num_ac': 1,
                            'num_ac_up': 1,
                        },
                        'pw': {
                            'num_pw': 1,
                            'num_pw_up': 1,
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        Device1# show l2vpn bridge-domain brief

        Bridge Group/Bridge-Domain Name  ID    State      Num ACs/up     Num PWs/up
        -------------------------------- ----- ---------- -------------- --------------
        g1/bd1                           0     up         1/1            1/1 
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnBridgeDomainBrief(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowL2vpnBridgeDomainBrief(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)

# =================================================
#  Unit test for 'show l2vpn bridge-domain detail'
# =================================================

class TestShowL2vpnBridgeDomainDetail(unittest.TestCase):
    '''Unit test for "show l2vpn bridge-domain detail"'''

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'bridge_group': {
            'g1': {
                'bridge_domain': {
                    'bd1': {
                        'state': 'up',
                        'id': 0,
                        'shg_id': 0,
                        'mst_i': 0,
                        'mac_learning': 'enabled',
                        'mac_withdraw': 'disabled',
                        'flooding': {
                            'broadcast_multicast': 'enabled',
                            'unknown_unicast': 'enabled',
                        },
                        'mac_aging_time': 300,
                        'mac_aging_type': 'inactivity',
                        'mac_limit': 4000,
                        'mac_limit_action': 'none',
                        'mac_limit_notification': 'syslog',
                        'mac_limit_reached': 'yes',
                        'security': 'disabled',
                        'dhcp_v4_snooping': 'disabled',
                        'mtu': 1500,
                        'ac': {
                            'num_ac': 1,
                            'num_ac_up': 1,
                            'interfaces': {
                                'GigabitEthernet0/1/0/0': {
                                    'state': 'up',
                                    'type': 'Ethernet',
                                    'mtu': 1500,
                                    'xc_id': '0x2000001',
                                    'interworking': 'none',
                                    'mst_i': 0,
                                    'mst_i_state': 'unprotected',
                                    'mac_learning': 'enabled',
                                    'flooding': {
                                        'broadcast_multicast': 'enabled',
                                        'unknown_unicast': 'enabled',
                                    },
                                    'mac_aging_time': 300,
                                    'mac_aging_type': 'inactivity',
                                    'mac_limit': 4000,
                                    'mac_limit_action': 'none',
                                    'mac_limit_notification': 'syslog',
                                    'mac_limit_reached': 'yes',
                                    'security': 'disabled',
                                    'dhcp_v4_snooping': 'disabled',
                                    'static_mac_address': ['0000.0000.0000', '0001.0002.0003'],
                                    'statistics': {
                                        'packet_totals': {
                                            'receive': 3919680,
                                            'send': 9328,
                                        },
                                        'byte_totals': {
                                            'receive': 305735040,
                                            'send': 15022146,
                                        },
                                    },
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 1,
                            '1': {
                                'neighbor': {
                                    '10.4.1.1': {
                                        'pw_id': {
                                            '1': {
                                                'state': 'up ( established )',
                                                'pw_class': 'mpls',
                                                'xc_id': '0xff000001',
                                                'encapsulation': 'MPLS',
                                                'protocol': 'LDP',
                                                'pw_type': 'Ethernet',
                                                'control_word': 'disabled',
                                                'interworking': 'none',
                                                'pw_backup_disable_delay': 0,
                                                'sequencing': 'not set',
                                                'mpls': {
                                                    'label': {
                                                        'local': '16003',
                                                        'remote': '16003',
                                                    },
                                                    'group_id': {
                                                        'local': '0x0',
                                                        'remote': '0x0',
                                                    },
                                                    'interface': {
                                                        'local': '1',
                                                        'remote': '1',
                                                    },
                                                    'mtu': {
                                                        'local': '1500',
                                                        'remote': '1500',
                                                    },
                                                    'control_word': {
                                                        'local': 'disabled',
                                                        'remote': 'disabled',
                                                    },
                                                    'pw_type': {
                                                        'local': 'Ethernet',
                                                        'remote': 'Ethernet',
                                                    },
                                                    'vccv_cv_type': {
                                                        'local': '0x2',
                                                        'remote': '0x2',
                                                        'local_type': ['LSP ping verification'],
                                                        'remote_type': ['LSP ping verification'],
                                                    },
                                                    'vccv_cc_type': {
                                                        'local': '0x2',
                                                        'remote': '0x2',
                                                        'local_type': ['router alert label'],
                                                        'remote_type': ['router alert label'],
                                                    },
                                                },
                                                'create_time': '12/03/2008 14:03:00 (17:17:30 ago)',
                                                'last_time_status_changed': '13/03/2008 05:57:58 (01:22:31 ago)',
                                                'mac_withdraw_message': {
                                                    'send': 0,
                                                    'receive': 0,
                                                },
                                                'statistics': {
                                                    'packet_totals': {
                                                        'receive': 3918814,
                                                        'send': 3918024,
                                                    },
                                                    'byte_totals': {
                                                        'receive': 305667492,
                                                        'send': 321277968,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'statistics': {
                                    'drop': {
                                        'illegal_vlan': 0,
                                        'illegal_length': 0,
                                    },
                                },
                            },
                        },
                        'pw': {
                            'num_pw': 1,
                            'num_pw_up': 1,
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        Bridge group: g1, bridge-domain: bd1, id: 0, state: up, ShgId: 0, MSTi: 0
        MAC learning: enabled
        MAC withdraw: disabled
        Flooding:
            Broadcast & Multicast: enabled
            Unknown unicast: enabled
        MAC aging time: 300 s, Type: inactivity
        MAC limit: 4000, Action: none, Notification: syslog
        MAC limit reached: yes
        Security: disabled
        DHCPv4 snooping: disabled
        MTU: 1500
        Filter MAC addresses:
        ACs: 1 (1 up), VFIs: 1, PWs: 1 (1 up)
        List of ACs:
            AC: GigabitEthernet0/1/0/0, state is up
            Type Ethernet
            MTU 1500; XC ID 0x2000001; interworking none; MSTi 0 (unprotected)
            MAC learning: enabled
            Flooding:
                Broadcast & Multicast: enabled
                Unknown unicast: enabled
            MAC aging time: 300 s, Type: inactivity
            MAC limit: 4000, Action: none, Notification: syslog
            MAC limit reached: yes
            Security: disabled
            DHCPv4 snooping: disabled
            Static MAC addresses:
                0000.0000.0000
                0001.0002.0003
            Statistics:
                packet totals: receive 3919680,send 9328
                byte totals: receive 305735040,send 15022146
        List of Access PWs:
        List of VFIs:
            VFI 1
            PW: neighbor 10.4.1.1, PW ID 1, state is up ( established )
                PW class mpls, XC ID 0xff000001
                Encapsulation MPLS, protocol LDP
                PW type Ethernet, control word disabled, interworking none
                PW backup disable delay 0 sec
                Sequencing not set
                        MPLS         Local                          Remote                        
                ------------ ------------------------------ -------------------------
                Label        16003                          16003                         
                Group ID     0x0                            0x0                           
                Interface    1                              1                             
                MTU          1500                           1500                          
                Control word disabled                       disabled                      
                PW type      Ethernet                       Ethernet                      
                VCCV CV type 0x2                            0x2                           
                             (LSP ping verification)        (LSP ping verification)       
                VCCV CC type 0x2                            0x2                           
                             (router alert label)           (router alert label)          
                ------------ ------------------------------ -------------------------
                Create time: 12/03/2008 14:03:00 (17:17:30 ago)
                Last time status changed: 13/03/2008 05:57:58 (01:22:31 ago)
                MAC withdraw message: send 0 receive 0
                Static MAC addresses:
                Statistics:
                packet totals: receive 3918814, send 3918024
                byte totals: receive 305667492, send 321277968
            VFI Statistics:
                drops: illegal VLAN 0, illegal length 0
    '''}

    golden_parsed_output2 = {
        'bridge_group': {
            'foo_group': {
                'bridge_domain': {
                    'foo_bd': {
                        'state': 'up',
                        'id': 0,
                        'shg_id': 0,
                        'mode': 'VPWS',
                        'mtu': 1500,
                        'ac': {
                            'num_ac': 1,
                            'num_ac_up': 0,
                            'interfaces': {
                                'GigabitEthernet0/5/1/4': {
                                    'state': 'admin down',
                                    'type': 'Ethernet',
                                    'mtu': 1500,
                                    'xc_id': '1',
                                    'interworking': 'none',
                                    'statistics': {
                                        'packet_totals': {
                                            'receive': 0,
                                            'send': 0,
                                        },
                                        'byte_totals': {
                                            'receive': 0,
                                            'send': 0,
                                        },
                                    },
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 1,
                            'foo_vfi': {
                                'neighbor': {
                                    '10.4.1.1': {
                                        'pw_id': {
                                            '1': {
                                                'state': 'up ( established )',
                                                'pw_class': 'not set',
                                                'encapsulation': 'MPLS',
                                                'protocol': 'LDP',
                                                'pw_type': 'Ethernet',
                                                'control_word': 'enabled',
                                                'interworking': 'none',
                                                'sequencing': 'not set',
                                                'mpls': {
                                                    'label': {
                                                        'local': '16001',
                                                        'remote': '16001',
                                                    },
                                                    'group_id': {
                                                        'local': 'unassigned',
                                                        'remote': 'unknown',
                                                    },
                                                    'interface': {
                                                        'local': 'siva/vfi',
                                                        'remote': 'siva/vfi',
                                                    },
                                                    'mtu': {
                                                        'local': '1500',
                                                        'remote': '1500',
                                                    },
                                                    'control_word': {
                                                        'local': 'enabled',
                                                        'remote': 'enabled',
                                                    },
                                                    'pw_type': {
                                                        'local': 'Ethernet',
                                                        'remote': 'Ethernet',
                                                    },
                                                    'vccv_cv_type': {
                                                        'local': '0x2',
                                                        'remote': '0x2',
                                                        'local_type': ['LSP ping verification'],
                                                        'remote_type': ['LSP ping verification'],
                                                    },
                                                    'vccv_cc_type': {
                                                        'local': '0x3',
                                                        'remote': '0x3',
                                                        'local_type': ['control word', 'router alert label'],
                                                        'remote_type': ['control word', 'router alert label'],
                                                    },
                                                },
                                                'create_time': '25/06/2007 05:29:42 (2w0d ago)',
                                                'last_time_status_changed': '27/06/2007 06:50:35 (1w5d ago)',
                                            },
                                            '2': {
                                                'state': 'up ( established )',
                                                'pw_class': 'not set',
                                                'encapsulation': 'MPLS',
                                                'protocol': 'LDP',
                                                'pw_type': 'Ethernet',
                                                'control_word': 'enabled',
                                                'interworking': 'none',
                                                'sequencing': 'not set',
                                                'mpls': {
                                                    'label': {
                                                        'local': '16002',
                                                        'remote': '16002',
                                                    },
                                                    'group_id': {
                                                        'local': 'unassigned',
                                                        'remote': 'unknown',
                                                    },
                                                    'monitor_interface': {
                                                        'local': 'siva/vfi',
                                                        'remote': 'siva/vfi',
                                                    },
                                                    'mtu': {
                                                        'local': '1500',
                                                        'remote': '1500',
                                                    },
                                                    'control_word': {
                                                        'local': 'enabled',
                                                        'remote': 'enabled',
                                                    },
                                                    'pw_type': {
                                                        'local': 'Ethernet',
                                                        'remote': 'Ethernet',
                                                    },
                                                    'vccv_cv_type': {
                                                        'local': '0x2',
                                                        'remote': '0x2',
                                                        'local_type': ['LSP ping verification'],
                                                        'remote_type': ['LSP ping verification'],
                                                    },
                                                    'vccv_cc_type': {
                                                        'local': '0x3',
                                                        'remote': '0x3',
                                                        'local_type': ['control word', 'router alert label'],
                                                        'remote_type': ['control word', 'router alert label'],
                                                    },
                                                },
                                                'create_time': '25/06/2007 05:29:42 (2w0d ago)',
                                                'last_time_status_changed': '27/06/2007 06:50:35 (1w5d ago)',
                                            },
                                        },
                                    },
                                },
                                'statistics': {
                                    'drop': {
                                        'illegal_vlan': 0,
                                        'illegal_length': 0,
                                    },
                                },
                            },
                        },
                        'pw': {
                            'num_pw': 2,
                            'num_pw_up': 2,
                        },
                    },
                },
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
        Bridge group: foo_group, bridge-domain: foo_bd, id: 0, state: up, ShgId: 0
        VPWS Mode
        MTU: 1500
        ACs: 1 (0 up), VFIs: 1, PWs: 2 (2 up)
        List of ACs:
            AC: GigabitEthernet0/5/1/4, state is admin down
            Type Ethernet      MTU 1500; XC ID 1; interworking none
            Static MAC addresses:
            Statistics:
                packet totals: receive 0,send 0
                byte totals: receive 0,send 0
        List of VFIs:
            VFI foo_vfi
            PW: neighbor 10.4.1.1, PW ID 1, state is up ( established )
                PW class not set
                Encapsulation MPLS, protocol LDP
                PW type Ethernet, control word enabled, interworking none
                Sequencing not set
                MPLS         Local                          Remote                        
                ------------ ------------------------------ ------------------------------
                Label        16001                          16001
                Group ID     unassigned                     unknown                       
                Interface    siva/vfi                       siva/vfi                      
                MTU          1500                           1500                          
                Control word enabled                        enabled                       
                PW type      Ethernet                       Ethernet                      
                VCCV CV type 0x2                            0x2                           
                             (LSP ping verification)        (LSP ping verification)       
                VCCV CC type 0x3                            0x3                           
                             (control word)                 (control word)                
                             (router alert label)           (router alert label)          
                ------------ ------------------------------ ------------------------------
                Create time: 25/06/2007 05:29:42 (2w0d ago)
                Last time status changed: 27/06/2007 06:50:35 (1w5d ago)
            Static MAC addresses:
            PW: neighbor 10.4.1.1, PW ID 2, state is up ( established )
                PW class not set
                Encapsulation MPLS, protocol LDP
                PW type Ethernet, control word enabled, interworking none
                Sequencing not set
                MPLS         Local                          Remote                        
                ------------ ------------------------------ ------------------------------
                Label        16002                          16002                         
                Group ID     unassigned                     unknown                       
                Interface    siva/vfi                       siva/vfi                      
                MTU          1500                           1500                          
                Control word enabled                        enabled                       
                PW type      Ethernet                       Ethernet                      
                VCCV CV type 0x2                            0x2                           
                            (LSP ping verification)        (LSP ping verification)       
                VCCV CC type 0x3                            0x3                           
                            (control word)                 (control word)                
                            (router alert label)           (router alert label)          
                ------------ ------------------------------ ------------------------------
                Create time: 25/06/2007 05:29:42 (2w0d ago)
                Last time status changed: 27/06/2007 06:50:35 (1w5d ago)
            Static MAC addresses:
            Statistics:
                drops: illegal VLAN 0, illegal length 0
    '''}

    golden_parsed_output3 = {
        'legend': 'pp = Partially Programmed.',
        'bridge_group': {
            'EVPN-Mulicast': {
                'bridge_domain': {
                    'EVPN-Multicast-BTV': {
                        'state': 'up',
                        'id': 0,
                        'shg_id': 0,
                        'mst_i': 0,
                        'coupled_state': 'disabled',
                        'vine_state': 'EVPN-IRB',
                        'mac_learning': 'enabled',
                        'mac_withdraw': 'enabled',
                        'mac_withdraw_for_access_pw': 'enabled',
                        'mac_withdraw_sent_on': 'bridge port up',
                        'mac_withdraw_relaying': 'disabled',
                        'flooding': {
                            'broadcast_multicast': 'enabled',
                            'unknown_unicast': 'enabled',
                        },
                        'mac_aging_time': 300,
                        'mac_aging_type': 'inactivity',
                        'mac_limit': 4000,
                        'mac_limit_action': 'none',
                        'mac_limit_notification': 'syslog',
                        'mac_limit_reached': 'no',
                        'mac_limit_threshold': '75%',
                        'mac_port_down_flush': 'enabled',
                        'mac_secure': 'disabled',
                        'mac_secure_logging': 'disabled',
                        'split_horizon_group': 'none',
                        'dynamic_arp_inspection': 'disabled',
                        'dynamic_arp_logging': 'disabled',
                        'ip_source_guard': 'disabled',
                        'ip_source_logging': 'disabled',
                        'dhcp_v4_snooping': 'disabled',
                        'dhcp_v4_snooping_profile': 'none',
                        'igmp_snooping': 'disabled',
                        'igmp_snooping_profile': 'none',
                        'mld_snooping_profile': 'none',
                        'storm_control': 'bridge-domain policer',
                        'bridge_mtu': '1500',
                        'mid_cvpls_config_index': '1',
                        'p2mp_pw': 'disabled',
                        'create_time': '27/08/2019 09:44:44 (5w6d ago)',
                        'status_changed_since_creation': 'No',
                        'ac': {
                            'num_ac': 3,
                            'num_ac_up': 2,
                            'interfaces': {
                                'BVI100': {
                                    'state': 'up',
                                    'type': 'Routed-Interface',
                                    'mtu': 1514,
                                    'xc_id': '0x8000000b',
                                    'interworking': 'none',
                                    'bvi_mac_address': ['1000.1000.1000'],
                                },
                                'Bundle-Ether3.100': {
                                    'state': 'down (Segment-down)',
                                    'type': 'VLAN',
                                    'vlan_num_ranges': '1',
                                    'rewrite_tags': '',
                                    'vlan_ranges': ['100', '100'],
                                    'mtu': 9202,
                                    'xc_id': '0xc0000002',
                                    'interworking': 'none',
                                    'mst_i': 5,
                                    'mac_learning': 'enabled',
                                    'flooding': {
                                        'broadcast_multicast': 'enabled',
                                        'unknown_unicast': 'enabled',
                                    },
                                    'mac_aging_time': 300,
                                    'mac_aging_type': 'inactivity',
                                    'mac_limit': 4000,
                                    'mac_limit_action': 'none',
                                    'mac_limit_notification': 'syslog',
                                    'mac_limit_reached': 'no',
                                    'mac_limit_threshold': '75%',
                                    'dhcp_v4_snooping': 'disabled',
                                    'dhcp_v4_snooping_profile': 'none',
                                    'igmp_snooping': 'disabled',
                                    'igmp_snooping_profile': 'none',
                                    'mld_snooping_profile': 'none',
                                },
                                'Bundle-Ether4.100': {
                                    'state': 'up',
                                    'type': 'VLAN',
                                    'vlan_num_ranges': '1',
                                    'rewrite_tags': '',
                                    'vlan_ranges': ['100', '100'],
                                    'mtu': 9202,
                                    'xc_id': '0xc0000004',
                                    'interworking': 'none',
                                    'mst_i': 5,
                                    'mac_learning': 'enabled',
                                    'flooding': {
                                        'broadcast_multicast': 'enabled',
                                        'unknown_unicast': 'enabled',
                                    },
                                    'mac_aging_time': 300,
                                    'mac_aging_type': 'inactivity',
                                    'mac_limit': 4000,
                                    'mac_limit_action': 'none',
                                    'mac_limit_notification': 'syslog',
                                    'mac_limit_reached': 'no',
                                    'mac_limit_threshold': '75%',
                                    'dhcp_v4_snooping': 'disabled',
                                    'dhcp_v4_snooping_profile': 'none',
                                    'igmp_snooping': 'disabled',
                                    'igmp_snooping_profile': 'none',
                                    'mld_snooping_profile': 'none',
                                    'statistics': {
                                        'packet_totals': {
                                            'receive': 1017635,
                                            'send': 798,
                                        },
                                        'byte_totals': {
                                            'receive': 73168116,
                                            'send': 36708,
                                        },
                                        'mac_move': '0',
                                    },
                                    'storm_control_drop_counters': {
                                        'packets': {
                                            'broadcast': '0',
                                            'multicast': '0',
                                            'unknown_unicast': '0',
                                        },
                                        'bytes': {
                                            'broadcast': '0',
                                            'multicast': '0',
                                            'unknown_unicast': '0',
                                        },
                                    },
                                    'dynamic_arp_inspection_drop_counters': {
                                        'packets': '0',
                                        'bytes': '0',
                                    },
                                    'ip_source_guard_drop_counters': {
                                        'packets': '0',
                                        'bytes': '0',
                                    },
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 0,
                        },
                        'pw': {
                            'num_pw': 0,
                            'num_pw_up': 0,
                        },
                        'pbb': {
                            'num_pbb': 0,
                            'num_pbb_up': 0,
                        },
                        'vni': {
                            'num_vni': 0,
                            'num_vni_up': 0,
                        },
                        'evpn': {
                            'EVPN': {
                                'state': 'up',
                                'evi': '1000',
                                'xc_id': '0x80000009',
                                'statistics': {
                                    'packet_totals': {
                                        'receive': 0,
                                        'send': 0,
                                    },
                                    'byte_totals': {
                                        'receive': 0,
                                        'send': 0,
                                    },
                                    'mac_move': '0',
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output3 = {'execute.return_value': '''
        show l2vpn bridge-domain detail

        Mon Oct  7 16:18:59.168 EDT
        Legend: pp = Partially Programmed.
        Bridge group: EVPN-Mulicast, bridge-domain: EVPN-Multicast-BTV, id: 0, state: up, ShgId: 0, MSTi: 0
        Coupled state: disabled
        VINE state: EVPN-IRB
        MAC learning: enabled
        MAC withdraw: enabled
            MAC withdraw for Access PW: enabled
            MAC withdraw sent on: bridge port up
            MAC withdraw relaying (access to access): disabled
        Flooding:
            Broadcast & Multicast: enabled
            Unknown unicast: enabled
        MAC aging time: 300 s, Type: inactivity
        MAC limit: 4000, Action: none, Notification: syslog
        MAC limit reached: no, threshold: 75%
        MAC port down flush: enabled
        MAC Secure: disabled, Logging: disabled
        Split Horizon Group: none
        Dynamic ARP Inspection: disabled, Logging: disabled
        IP Source Guard: disabled, Logging: disabled
        DHCPv4 Snooping: disabled
        DHCPv4 Snooping profile: none
        IGMP Snooping: disabled
        IGMP Snooping profile: none
        MLD Snooping profile: none
        Storm Control: disabled
        Bridge MTU: 1500
        MIB cvplsConfigIndex: 1
        Filter MAC addresses:
        P2MP PW: disabled
        Create time: 27/08/2019 09:44:44 (5w6d ago)
        No status change since creation
        ACs: 3 (2 up), VFIs: 0, PWs: 0 (0 up), PBBs: 0 (0 up), VNIs: 0 (0 up)
        List of EVPNs:
            EVPN, state: up
            evi: 1000
            XC ID 0x80000009
            Statistics:
            packets: received 0 (unicast 0), sent 0
            bytes: received 0 (unicast 0), sent 0
            MAC move: 0
        List of ACs:
            AC: BVI100, state is up
            Type Routed-Interface
            MTU 1514; XC ID 0x8000000b; interworking none
            BVI MAC address:
                1000.1000.1000
            Split Horizon Group: Access
            AC: Bundle-Ether3.100, state is down (Segment-down)
            Type VLAN; Num Ranges: 1
            Rewrite Tags: []
            VLAN ranges: [100, 100]
            MTU 9202; XC ID 0xc0000002; interworking none; MSTi 5
            MAC learning: enabled
            Flooding:
                Broadcast & Multicast: enabled
                Unknown unicast: enabled
            MAC aging time: 300 s, Type: inactivity
            MAC limit: 4000, Action: none, Notification: syslog
            MAC limit reached: no, threshold: 75%
            MAC port down flush: enabled
            MAC Secure: disabled, Logging: disabled
            Split Horizon Group: none
            Dynamic ARP Inspection: disabled, Logging: disabled
            IP Source Guard: disabled, Logging: disabled
            DHCPv4 Snooping: disabled
            DHCPv4 Snooping profile: none
            IGMP Snooping: disabled
            IGMP Snooping profile: none
            MLD Snooping profile: none
            Storm Control: bridge-domain policer
            Static MAC addresses:
            AC: Bundle-Ether4.100, state is up
            Type VLAN; Num Ranges: 1
            Rewrite Tags: []
            VLAN ranges: [100, 100]
            MTU 9202; XC ID 0xc0000004; interworking none; MSTi 5
            MAC learning: enabled
            Flooding:
                Broadcast & Multicast: enabled
                Unknown unicast: enabled
            MAC aging time: 300 s, Type: inactivity
            MAC limit: 4000, Action: none, Notification: syslog
            MAC limit reached: no, threshold: 75%
            MAC port down flush: enabled
            MAC Secure: disabled, Logging: disabled
            Split Horizon Group: none
            Dynamic ARP Inspection: disabled, Logging: disabled
            IP Source Guard: disabled, Logging: disabled
            DHCPv4 Snooping: disabled
            DHCPv4 Snooping profile: none
            IGMP Snooping: disabled
            IGMP Snooping profile: none
            MLD Snooping profile: none
            Storm Control: bridge-domain policer
            Static MAC addresses:
            Statistics:
                packets: received 1017635 (multicast 1016837, broadcast 798, unknown unicast 0, unicast 0), sent 798
                bytes: received 73168116 (multicast 73120236, broadcast 47880, unknown unicast 0, unicast 0), sent 36708
                MAC move: 0
            Storm control drop counters: 
                packets: broadcast 0, multicast 0, unknown unicast 0 
                bytes: broadcast 0, multicast 0, unknown unicast 0 
            Dynamic ARP inspection drop counters: 
                packets: 0, bytes: 0
            IP source guard drop counters: 
                packets: 0, bytes: 0
        List of Access PWs:
        List of VFIs:
        List of Access VFIs:
        RP/0/RSP0/CPU0:genie-Router#
    '''}

    golden_output4 = {'execute.return_value': '''
        show l2vpn bridge-domain detail

        Mon Oct 14 17:43:20.059 EDT
        Legend: pp = Partially Programmed.
        Bridge group: midlay, bridge-domain: bd601, id: 0, state: up, ShgId: 0, MSTi: 0
        Coupled state: disabled
        VINE state: BVI Resolved
        MAC learning: enabled
        MAC withdraw: enabled
            MAC withdraw for Access PW: enabled
            MAC withdraw sent on: bridge port up
            MAC withdraw relaying (access to access): disabled
        Flooding:
            Broadcast & Multicast: enabled
            Unknown unicast: enabled
        MAC aging time: 300 s, Type: inactivity
        MAC limit: 4000, Action: none, Notification: syslog
        MAC limit reached: no, threshold: 75%
        MAC port down flush: enabled
        MAC Secure: disabled, Logging: disabled
        Split Horizon Group: none
        Dynamic ARP Inspection: disabled, Logging: disabled
        IP Source Guard: disabled, Logging: disabled
        DHCPv4 Snooping: disabled
        DHCPv4 Snooping profile: none
        IGMP Snooping: disabled
        IGMP Snooping profile: none
        MLD Snooping profile: none
        Storm Control: disabled
        Bridge MTU: 1500
        MIB cvplsConfigIndex: 1
        Filter MAC addresses:
        P2MP PW: disabled
        Create time: 11/07/2019 13:01:43 (13w4d ago)
        No status change since creation
        ACs: 1 (0 up), VFIs: 0, PWs: 1 (0 up), PBBs: 0 (0 up), VNIs: 0 (0 up)
        List of ACs:
            AC: BVI601, state is down (Segment-down)
            Type Routed-Interface
            MTU 1514; XC ID 0x8000000d; interworking none
            Error: Need at least 1 bridge port up
            BVI MAC address:
                00c1.6474.81ca
            Split Horizon Group: Access
        List of Access PWs:
            EVPN: neighbor 0.0.0.0, PW ID: evi 601, ac-id 1, state is down ( local ready ) (Transport LSP Down)
            XC ID 0xa0000009
            Encapsulation MPLS
            Source address 10.154.219.85
            Encap type Ethernet, control word enabled
            Sequencing not set
            LSP : Up

                EVPN         Local                          Remote                        
                ------------ ------------------------------ ---------------------------
                Label        100482                         unknown                       
                MTU          1500                           unknown                       
                Control word enabled                        unknown                       
                AC ID        1                              1                             
                EVPN type    Ethernet                       unknown                       

                ------------ ------------------------------ ---------------------------
            Create time: 11/07/2019 13:01:43 (13w4d ago)
            Last time status changed: 11/07/2019 13:06:41 (13w4d ago)
            MAC withdraw messages: sent 0, received 0
            Forward-class: 0
            Static MAC addresses:
            MAC learning: enabled
            Flooding:
                Broadcast & Multicast: enabled
                Unknown unicast: enabled
            MAC aging time: 300 s, Type: inactivity
            MAC limit: 4000, Action: none, Notification: syslog
            MAC limit reached: no, threshold: 75%
            MAC port down flush: enabled
            MAC Secure: disabled, Logging: disabled
            Split Horizon Group: none
            DHCPv4 Snooping: disabled
            DHCPv4 Snooping profile: none
            IGMP Snooping: disabled
            IGMP Snooping profile: none
            MLD Snooping profile: none
            Storm Control: bridge-domain policer
        List of VFIs:
        List of Access VFIs:
        Bridge group: EVPN-Mulicast, bridge-domain: EVPN-Multicast-BTV, id: 1, state: up, ShgId: 0, MSTi: 0
        Coupled state: disabled
        VINE state: EVPN-IRB
        MAC learning: enabled
        MAC withdraw: enabled
            MAC withdraw for Access PW: enabled
            MAC withdraw sent on: bridge port up
            MAC withdraw relaying (access to access): disabled
        Flooding:
            Broadcast & Multicast: enabled
            Unknown unicast: enabled
        MAC aging time: 300 s, Type: inactivity
        MAC limit: 4000, Action: none, Notification: syslog
        MAC limit reached: no, threshold: 75%
        MAC port down flush: enabled
        MAC Secure: disabled, Logging: disabled
        Split Horizon Group: none
        Dynamic ARP Inspection: disabled, Logging: disabled
        IP Source Guard: disabled, Logging: disabled
        DHCPv4 Snooping: disabled
        DHCPv4 Snooping profile: none
        IGMP Snooping: disabled
        IGMP Snooping profile: none
        MLD Snooping profile: none
        Storm Control: disabled
        Bridge MTU: 1500
        MIB cvplsConfigIndex: 2
        Filter MAC addresses:
        P2MP PW: disabled
        Create time: 11/07/2019 13:01:43 (13w4d ago)
        No status change since creation
        ACs: 3 (0 up), VFIs: 0, PWs: 0 (0 up), PBBs: 0 (0 up), VNIs: 0 (0 up)
        List of EVPNs:
            EVPN, state: up
            evi: 1000
            XC ID 0x80000007
            Statistics:
            packets: received 10305221406 (unicast 74), sent 41020743245
            bytes: received 10474510995022 (unicast 3108), sent 41841158015034
            MAC move: 0
        List of ACs:
            AC: BVI100, state is down (Segment-down)
            Type Routed-Interface
            MTU 1514; XC ID 0x8000000b; interworking none
            Error: Need at least 1 bridge port up
            BVI MAC address:
                1000.1000.1000
            Split Horizon Group: Access
            AC: Bundle-Ether3.100, state is down (Segment-down)
            Type VLAN; Num Ranges: 1
            Rewrite Tags: []
            VLAN ranges: [100, 100]
            MTU 9202; XC ID 0xc0000004; interworking none; MSTi 5
            MAC learning: enabled
            Flooding:
                Broadcast & Multicast: enabled
                Unknown unicast: enabled
            MAC aging time: 300 s, Type: inactivity
            MAC limit: 4000, Action: none, Notification: syslog
            MAC limit reached: no, threshold: 75%
            MAC port down flush: enabled
            MAC Secure: disabled, Logging: disabled
            Split Horizon Group: none
            Dynamic ARP Inspection: disabled, Logging: disabled
            IP Source Guard: disabled, Logging: disabled
            DHCPv4 Snooping: disabled
            DHCPv4 Snooping profile: none
            IGMP Snooping: disabled
            IGMP Snooping profile: none
            MLD Snooping profile: none
            Storm Control: bridge-domain policer
            Static MAC addresses:
            AC: Bundle-Ether4.100, state is down (Segment-down)
            Type VLAN; Num Ranges: 1
            Rewrite Tags: []
            VLAN ranges: [100, 100]
            MTU 9202; XC ID 0xc0000006; interworking none; MSTi 5
            MAC learning: enabled
            Flooding:
                Broadcast & Multicast: enabled
                Unknown unicast: enabled
            MAC aging time: 300 s, Type: inactivity
            MAC limit: 4000, Action: none, Notification: syslog
            MAC limit reached: no, threshold: 75%
            MAC port down flush: enabled
            MAC Secure: disabled, Logging: disabled
            Split Horizon Group: none
            Dynamic ARP Inspection: disabled, Logging: disabled
            IP Source Guard: disabled, Logging: disabled
            DHCPv4 Snooping: disabled
            DHCPv4 Snooping profile: none
            IGMP Snooping: disabled
            IGMP Snooping profile: none
            MLD Snooping profile: none
            Storm Control: bridge-domain policer
            Static MAC addresses:
        List of Access PWs:
        List of VFIs:
        List of Access VFIs:

    '''}

    golden_parsed_output4 = {
        'legend': 'pp = Partially Programmed.',
        'bridge_group': {
            'midlay': {
                'bridge_domain': {
                    'bd601': {
                        'state': 'up',
                        'id': 0,
                        'shg_id': 0,
                        'mst_i': 0,
                        'coupled_state': 'disabled',
                        'vine_state': 'BVI',
                        'mac_learning': 'enabled',
                        'mac_withdraw': 'enabled',
                        'mac_withdraw_for_access_pw': 'enabled',
                        'mac_withdraw_sent_on': 'bridge port up',
                        'mac_withdraw_relaying': 'disabled',
                        'flooding': {
                            'broadcast_multicast': 'enabled',
                            'unknown_unicast': 'enabled',
                        },
                        'mac_aging_time': 300,
                        'mac_aging_type': 'inactivity',
                        'mac_limit': 4000,
                        'mac_limit_action': 'none',
                        'mac_limit_notification': 'syslog',
                        'mac_limit_reached': 'no',
                        'mac_limit_threshold': '75%',
                        'mac_port_down_flush': 'enabled',
                        'mac_secure': 'disabled',
                        'mac_secure_logging': 'disabled',
                        'split_horizon_group': 'Access',
                        'dynamic_arp_inspection': 'disabled',
                        'dynamic_arp_logging': 'disabled',
                        'ip_source_guard': 'disabled',
                        'ip_source_logging': 'disabled',
                        'dhcp_v4_snooping': 'disabled',
                        'dhcp_v4_snooping_profile': 'none',
                        'igmp_snooping': 'disabled',
                        'igmp_snooping_profile': 'none',
                        'mld_snooping_profile': 'none',
                        'storm_control': 'disabled',
                        'bridge_mtu': '1500',
                        'mid_cvpls_config_index': '1',
                        'p2mp_pw': 'disabled',
                        'create_time': '11/07/2019 13:01:43 (13w4d ago)',
                        'status_changed_since_creation': 'No',
                        'ac': {
                            'num_ac': 1,
                            'num_ac_up': 0,
                            'interfaces': {
                                'BVI601': {
                                    'state': 'down (Segment-down)',
                                    'type': 'Routed-Interface',
                                    'mtu': 1514,
                                    'xc_id': '0x8000000d',
                                    'interworking': 'none',
                                    'error': 'Need at least 1 bridge port up',
                                    'bvi_mac_address': ['00c1.6474.81ca'],
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 0,
                        },
                        'pw': {
                            'num_pw': 1,
                            'num_pw_up': 0,
                        },
                        'pbb': {
                            'num_pbb': 0,
                            'num_pbb_up': 0,
                        },
                        'vni': {
                            'num_vni': 0,
                            'num_vni_up': 0,
                        },
                        'access_pw': {
                            'EVPN': {
                                'neighbor': {
                                    '0.0.0.0': {
                                        'pw_id': {
                                            'evi 601': {
                                                'ac_id': '1',
                                                'state': 'down ( local ready ) (Transport LSP Down)',
                                                'xc_id': '0xa0000009',
                                                'encapsulation': 'MPLS',
                                                'source_address': '10.154.219.85',
                                                'encap_type': 'Ethernet',
                                                'control_word': 'enabled',
                                                'sequencing': 'not set',
                                                'lsp': {
                                                    'state': 'Up',
                                                    'evpn': {
                                                        'label': {
                                                            'local': '100482',
                                                            'remote': 'unknown',
                                                        },
                                                        'mtu': {
                                                            'local': '1500',
                                                            'remote': 'unknown',
                                                        },
                                                        'control_word': {
                                                            'local': 'enabled',
                                                            'remote': 'unknown',
                                                        },
                                                        'ac_id': {
                                                            'local': '1',
                                                            'remote': '1',
                                                        },
                                                        'evpn_type': {
                                                            'local': 'Ethernet',
                                                            'remote': 'unknown',
                                                        },
                                                    },
                                                },
                                                'create_time': '11/07/2019 13:01:43 (13w4d ago)',
                                                'last_time_status_changed': '11/07/2019 13:06:41 (13w4d ago)',
                                                'mac_withdraw_message': {
                                                    'send': 0,
                                                    'receive': 0,
                                                },
                                                'forward_class': '0',
                                                'mac_learning': 'enabled',
                                                'flooding': {
                                                    'broadcast_multicast': 'enabled',
                                                    'unknown_unicast': 'enabled',
                                                },
                                                'mac_aging_time': 300,
                                                'mac_aging_type': 'inactivity',
                                                'mac_limit': 4000,
                                                'mac_limit_action': 'none',
                                                'mac_limit_notification': 'syslog',
                                                'mac_limit_reached': 'no',
                                                'mac_limit_threshold': '75%',
                                                'mac_port_down_flush': 'enabled',
                                                'mac_secure': 'disabled',
                                                'mac_secure_logging': 'disabled',
                                                'split_horizon_group': 'none',
                                                'dhcp_v4_snooping': 'disabled',
                                                'dhcp_v4_snooping_profile': 'none',
                                                'igmp_snooping': 'disabled',
                                                'igmp_snooping_profile': 'none',
                                                'mld_snooping_profile': 'none',
                                                'storm_control': 'bridge-domain policer',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'EVPN-Mulicast': {
                'bridge_domain': {
                    'EVPN-Multicast-BTV': {
                        'state': 'up',
                        'id': 1,
                        'shg_id': 0,
                        'mst_i': 0,
                        'coupled_state': 'disabled',
                        'vine_state': 'EVPN-IRB',
                        'mac_learning': 'enabled',
                        'mac_withdraw': 'enabled',
                        'mac_withdraw_for_access_pw': 'enabled',
                        'mac_withdraw_sent_on': 'bridge port up',
                        'mac_withdraw_relaying': 'disabled',
                        'flooding': {
                            'broadcast_multicast': 'enabled',
                            'unknown_unicast': 'enabled',
                        },
                        'mac_aging_time': 300,
                        'mac_aging_type': 'inactivity',
                        'mac_limit': 4000,
                        'mac_limit_action': 'none',
                        'mac_limit_notification': 'syslog',
                        'mac_limit_reached': 'no',
                        'mac_limit_threshold': '75%',
                        'mac_port_down_flush': 'enabled',
                        'mac_secure': 'disabled',
                        'mac_secure_logging': 'disabled',
                        'split_horizon_group': 'none',
                        'dynamic_arp_inspection': 'disabled',
                        'dynamic_arp_logging': 'disabled',
                        'ip_source_guard': 'disabled',
                        'ip_source_logging': 'disabled',
                        'dhcp_v4_snooping': 'disabled',
                        'dhcp_v4_snooping_profile': 'none',
                        'igmp_snooping': 'disabled',
                        'igmp_snooping_profile': 'none',
                        'mld_snooping_profile': 'none',
                        'storm_control': 'bridge-domain policer',
                        'bridge_mtu': '1500',
                        'mid_cvpls_config_index': '2',
                        'p2mp_pw': 'disabled',
                        'create_time': '11/07/2019 13:01:43 (13w4d ago)',
                        'status_changed_since_creation': 'No',
                        'ac': {
                            'num_ac': 3,
                            'num_ac_up': 0,
                            'interfaces': {
                                'BVI100': {
                                    'state': 'down (Segment-down)',
                                    'type': 'Routed-Interface',
                                    'mtu': 1514,
                                    'xc_id': '0x8000000b',
                                    'interworking': 'none',
                                    'error': 'Need at least 1 bridge port up',
                                    'bvi_mac_address': ['1000.1000.1000'],
                                },
                                'Bundle-Ether3.100': {
                                    'state': 'down (Segment-down)',
                                    'type': 'VLAN',
                                    'vlan_num_ranges': '1',
                                    'rewrite_tags': '',
                                    'vlan_ranges': ['100', '100'],
                                    'mtu': 9202,
                                    'xc_id': '0xc0000004',
                                    'interworking': 'none',
                                    'mst_i': 5,
                                    'mac_learning': 'enabled',
                                    'flooding': {
                                        'broadcast_multicast': 'enabled',
                                        'unknown_unicast': 'enabled',
                                    },
                                    'mac_aging_time': 300,
                                    'mac_aging_type': 'inactivity',
                                    'mac_limit': 4000,
                                    'mac_limit_action': 'none',
                                    'mac_limit_notification': 'syslog',
                                    'mac_limit_reached': 'no',
                                    'mac_limit_threshold': '75%',
                                    'dhcp_v4_snooping': 'disabled',
                                    'dhcp_v4_snooping_profile': 'none',
                                    'igmp_snooping': 'disabled',
                                    'igmp_snooping_profile': 'none',
                                    'mld_snooping_profile': 'none',
                                },
                                'Bundle-Ether4.100': {
                                    'state': 'down (Segment-down)',
                                    'type': 'VLAN',
                                    'vlan_num_ranges': '1',
                                    'rewrite_tags': '',
                                    'vlan_ranges': ['100', '100'],
                                    'mtu': 9202,
                                    'xc_id': '0xc0000006',
                                    'interworking': 'none',
                                    'mst_i': 5,
                                    'mac_learning': 'enabled',
                                    'flooding': {
                                        'broadcast_multicast': 'enabled',
                                        'unknown_unicast': 'enabled',
                                    },
                                    'mac_aging_time': 300,
                                    'mac_aging_type': 'inactivity',
                                    'mac_limit': 4000,
                                    'mac_limit_action': 'none',
                                    'mac_limit_notification': 'syslog',
                                    'mac_limit_reached': 'no',
                                    'mac_limit_threshold': '75%',
                                    'dhcp_v4_snooping': 'disabled',
                                    'dhcp_v4_snooping_profile': 'none',
                                    'igmp_snooping': 'disabled',
                                    'igmp_snooping_profile': 'none',
                                    'mld_snooping_profile': 'none',
                                },
                            },
                        },
                        'vfi': {
                            'num_vfi': 0,
                        },
                        'pw': {
                            'num_pw': 0,
                            'num_pw_up': 0,
                        },
                        'pbb': {
                            'num_pbb': 0,
                            'num_pbb_up': 0,
                        },
                        'vni': {
                            'num_vni': 0,
                            'num_vni_up': 0,
                        },
                        'evpn': {
                            'EVPN': {
                                'state': 'up',
                                'evi': '1000',
                                'xc_id': '0x80000007',
                                'statistics': {
                                    'packet_totals': {
                                        'receive': 10305221406,
                                        'send': 41020743245,
                                    },
                                    'byte_totals': {
                                        'receive': 10474510995022,
                                        'send': 41841158015034,
                                    },
                                    'mac_move': '0',
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnBridgeDomainDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowL2vpnBridgeDomainDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)

    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowL2vpnBridgeDomainDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output2)
    
    def test_golden3(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output3)
        obj = ShowL2vpnBridgeDomainDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output3)
    
    def test_golden4(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output4)
        obj = ShowL2vpnBridgeDomainDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output4)
        
if __name__ == '__main__':
    unittest.main()