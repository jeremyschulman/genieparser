import re
import unittest
from unittest.mock import Mock

from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
                                             SchemaMissingKeyError

from genie.libs.parser.iosxr.show_ipv6 import ShowIpv6NeighborsDetail, ShowIpv6Neighbors


#############################################################################
# unitest For show ipv6 neighbors detail
#############################################################################

class test_show_ipv6_neighbors_detail(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'interfaces': {
            'GigabitEthernet0/0/0/0': {
                'interface': 'GigabitEthernet0/0/0/0',
                'neighbors': {
                    '2010:1:2::1': {
                        'age': '82',
                        'ip': '2010:1:2::1',
                        'link_layer_address': 'fa16.3e19.abba',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    '2010:1:2::22': {
                        'age': '-',
                        'ip': '2010:1:2::22',
                        'link_layer_address': 'aaaa.beaf.bbbb',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': 'Y',
                        'dynamic': '-',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'static',
                    },
                    'fe80::f816:3eff:fe19:abba': {
                        'age': '158',
                        'ip': 'fe80::f816:3eff:fe19:abba',
                        'link_layer_address': 'fa16.3e19.abba',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': '-',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'other',
                    },
                },
            },
            'GigabitEthernet0/0/0/3': {
                'interface': 'GigabitEthernet0/0/0/3',
                'neighbors': {
                    '2020:2:3::3': {
                        'age': '114',
                        'ip': '2020:2:3::3',
                        'link_layer_address': '5e01.c002.0007',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    'fe80::5c01:c0ff:fe02:7': {
                        'age': '12',
                        'ip': 'fe80::5c01:c0ff:fe02:7',
                        'link_layer_address': '5e01.c002.0007',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': '-',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'other',
                    },
                },
            },
            'GigabitEthernet0/0/0/2': {
                'interface': 'GigabitEthernet0/0/0/2',
                'neighbors': {
                    '2010:2:3::3': {
                        'age': '1',
                        'ip': '2010:2:3::3',
                        'link_layer_address': '5e01.c002.0007',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    'fe80::5c01:c0ff:fe02:7': {
                        'age': '12',
                        'ip': 'fe80::5c01:c0ff:fe02:7',
                        'link_layer_address': '5e01.c002.0007',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': '-',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'other',
                    },
                },
            },
            'GigabitEthernet0/0/0/1': {
                'interface': 'GigabitEthernet0/0/0/1',
                'neighbors': {
                    '2020:1:2::1': {
                        'age': '4',
                        'ip': '2020:1:2::1',
                        'link_layer_address': 'fa16.3e72.8407',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    '2020:1:2::22': {
                        'age': '-',
                        'ip': '2020:1:2::22',
                        'link_layer_address': 'dddd.beef.aaaa',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': 'Y',
                        'dynamic': '-',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'static',
                    },
                    'fe80::f816:3eff:fe72:8407': {
                        'age': '37',
                        'ip': 'fe80::f816:3eff:fe72:8407',
                        'link_layer_address': 'fa16.3e72.8407',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': 'Y',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'dynamic',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                        'static': '-',
                        'dynamic': '-',
                        'sync': '-',
                        'serg_flags': 'ff',
                        'origin': 'other',
                    },
                },
            },
        },
    }

    golden_output = {'execute.return_value': '''
        RP/0/RP0/CPU0:xr9kv-2#show ipv6 neighbors detail
        Thu Apr 26 13:09:53.379 UTC
        IPv6 Address                             Age  Link-layer Add State Interface            Location      Static Dynamic Sync       Serg-Flags 
        2010:1:2::1                              82   fa16.3e19.abba REACH Gi0/0/0/0            0/0/CPU0        -      Y       -            ff
        2010:1:2::22                                - aaaa.beaf.bbbb REACH Gi0/0/0/0            0/0/CPU0        Y      -       -            ff
        fe80::f816:3eff:fe19:abba                158  fa16.3e19.abba REACH Gi0/0/0/0            0/0/CPU0        -      Y       -            ff
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0            0/0/CPU0        -      -       -            ff
        2020:2:3::3                              114  5e01.c002.0007 REACH Gi0/0/0/3            0/0/CPU0        -      Y       -            ff
        fe80::5c01:c0ff:fe02:7                   12   5e01.c002.0007 REACH Gi0/0/0/3            0/0/CPU0        -      Y       -            ff
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/3            0/0/CPU0        -      -       -            ff
        2010:2:3::3                              1    5e01.c002.0007 REACH Gi0/0/0/2            0/0/CPU0        -      Y       -            ff
        fe80::5c01:c0ff:fe02:7                   12   5e01.c002.0007 REACH Gi0/0/0/2            0/0/CPU0        -      Y       -            ff
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/2            0/0/CPU0        -      -       -            ff
        2020:1:2::1                              4    fa16.3e72.8407 REACH Gi0/0/0/1            0/0/CPU0        -      Y       -            ff
        2020:1:2::22                                - dddd.beef.aaaa REACH Gi0/0/0/1            0/0/CPU0        Y      -       -            ff
        fe80::f816:3eff:fe72:8407                37   fa16.3e72.8407 REACH Gi0/0/0/1            0/0/CPU0        -      Y       -            ff
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/1            0/0/CPU0        -      -       -            ff
    '''}

    def test_show_ipv6_neighbors_detail_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6NeighborsDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_ipv6_neighbors_detail_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowIpv6NeighborsDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


#############################################################################
# unitest For show ipv6 neighbors
#############################################################################

class TestShowIpv6Neighbors(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'interfaces': {
            'GigabitEthernet0/0/0/0.90': {
                'interface': 'GigabitEthernet0/0/0/0.90',
                'neighbors': {
                    'fe80::f816:3eff:fe26:1224': {
                        'age': '119',
                        'ip': 'fe80::f816:3eff:fe26:1224',
                        'link_layer_address': 'fa16.3e26.1224',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/1.90': {
                'interface': 'GigabitEthernet0/0/0/1.90',
                'neighbors': {
                    'fe80::5c00:40ff:fe02:7': {
                        'age': '128',
                        'ip': 'fe80::5c00:40ff:fe02:7',
                        'link_layer_address': '5e00.4002.0007',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/0.110': {
                'interface': 'GigabitEthernet0/0/0/0.110',
                'neighbors': {
                    'fe80::f816:3eff:fe26:1224': {
                        'age': '94',
                        'ip': 'fe80::f816:3eff:fe26:1224',
                        'link_layer_address': 'fa16.3e26.1224',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/0.115': {
                'interface': 'GigabitEthernet0/0/0/0.115',
                'neighbors': {
                    'fe80::f816:3eff:fe26:1224': {
                        'age': '27',
                        'ip': 'fe80::f816:3eff:fe26:1224',
                        'link_layer_address': 'fa16.3e26.1224',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/0.120': {
                'interface': 'GigabitEthernet0/0/0/0.120',
                'neighbors': {
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
        },
    }
    golden_output = {'execute.return_value': '''
        RP/0/RP0/CPU0:R2_xr#show ipv6 neighbors
        Thu Sep 26 22:11:10.340 UTC
        IPv6 Address                             Age  Link-layer Add State Interface            Location
        fe80::f816:3eff:fe26:1224                119  fa16.3e26.1224 REACH Gi0/0/0/0.90         0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.90         0/0/CPU0
        fe80::5c00:40ff:fe02:7                   128  5e00.4002.0007 REACH Gi0/0/0/1.90         0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/1.90         0/0/CPU0
        fe80::f816:3eff:fe26:1224                94   fa16.3e26.1224 REACH Gi0/0/0/0.110        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.110        0/0/CPU0
        fe80::f816:3eff:fe26:1224                27   fa16.3e26.1224 REACH Gi0/0/0/0.115        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.115        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.120        0/0/CPU0
    '''}

    golden_parsed_output1 = {
        'interfaces': {
            'GigabitEthernet0/0/0/0.390': {
                'interface': 'GigabitEthernet0/0/0/0.390',
                'neighbors': {
                    'fe80::f816:3eff:fe26:1224': {
                        'age': '47',
                        'ip': 'fe80::f816:3eff:fe26:1224',
                        'link_layer_address': 'fa16.3e26.1224',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
        },
    }
    golden_output1 = {'execute.return_value': '''
        RP/0/RP0/CPU0:R2_xr# show ipv6 neighbors vrf VRF1 Gi0/0/0/0.390
        Thu Sep 26 22:12:55.701 UTC
        IPv6 Address                             Age  Link-layer Add State Interface            Location
        fe80::f816:3eff:fe26:1224                47   fa16.3e26.1224 REACH Gi0/0/0/0.390        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.390        0/0/CPU0
    '''}

    golden_parsed_output2 = {
        'interfaces': {
            'GigabitEthernet0/0/0/0.390': {
                'interface': 'GigabitEthernet0/0/0/0.390',
                'neighbors': {
                    'fe80::f816:3eff:fe26:1224': {
                        'age': '90',
                        'ip': 'fe80::f816:3eff:fe26:1224',
                        'link_layer_address': 'fa16.3e26.1224',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/0.410': {
                'interface': 'GigabitEthernet0/0/0/0.410',
                'neighbors': {
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/0.415': {
                'interface': 'GigabitEthernet0/0/0/0.415',
                'neighbors': {
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
            'GigabitEthernet0/0/0/0.420': {
                'interface': 'GigabitEthernet0/0/0/0.420',
                'neighbors': {
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
        },
    }
    golden_output2 = {'execute.return_value': '''
        RP/0/RP0/CPU0:R2_xr#show ipv6 neighbors vrf VRF1
        Thu Sep 26 22:13:39.221 UTC
        IPv6 Address                             Age  Link-layer Add State Interface            Location
        fe80::f816:3eff:fe26:1224                90   fa16.3e26.1224 REACH Gi0/0/0/0.390        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.390        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.410        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.415        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.420        0/0/CPU0
    '''}

    golden_parsed_output3 = {
        'interfaces': {
            'GigabitEthernet0/0/0/0.390': {
                'interface': 'GigabitEthernet0/0/0/0.390',
                'neighbors': {
                    'fe80::f816:3eff:fe26:1224': {
                        'age': '129',
                        'ip': 'fe80::f816:3eff:fe26:1224',
                        'link_layer_address': 'fa16.3e26.1224',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                    'Mcast adjacency': {
                        'age': '-',
                        'ip': 'Mcast adjacency',
                        'link_layer_address': '0000.0000.0000',
                        'neighbor_state': 'REACH',
                        'location': '0/0/CPU0',
                    },
                },
            },
        },
    }
    golden_output3 = {'execute.return_value': '''
        RP/0/RP0/CPU0:R2_xr#show ipv6 neighbors Gi0/0/0/0.390
        Thu Sep 26 22:14:18.343 UTC
        IPv6 Address                             Age  Link-layer Add State Interface            Location
        fe80::f816:3eff:fe26:1224                129  fa16.3e26.1224 REACH Gi0/0/0/0.390        0/0/CPU0
        [Mcast adjacency]                           - 0000.0000.0000 REACH Gi0/0/0/0.390        0/0/CPU0
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6Neighbors(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)
    
    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse(vrf='VRF1', interface='Gi0/0/0/0.390')
        self.assertEqual(parsed_output, self.golden_parsed_output1)

    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse(vrf='VRF1')
        self.assertEqual(parsed_output, self.golden_parsed_output2)
    
    def test_golden3(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output3)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse(interface='Gi0/0/0/0.390')
        self.assertEqual(parsed_output, self.golden_parsed_output3)


if __name__ == '__main__':
    unittest.main()