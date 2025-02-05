# Python
import unittest
from unittest.mock import Mock
from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.parser.iosxr.show_xconnect import (ShowL2vpnXconnect,
                                                   ShowL2vpnXconnectDetail,
                                                   ShowL2vpnXconnectSummary,
                                                   ShowL2VpnXconnectBrief,
                                                   ShowL2vpnXconnectMp2mpDetail)

# ==========================================
#  Unit test for 'show l2vpn xconnect brief'
# ==========================================
class TestShowL2vpnXconnectBrief(unittest.TestCase):
    '''Unit test for 'show l2vpn xconnect brief' '''

    maxDiff = None
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'atom': 
            {'like_to_like': 
                {'efp': 
                    {'down': 0,
                    'unr': 0,
                    'up': 10},
                'total': 
                    {'down': 0,
                    'unr': 0,
                    'up': 10}},
            'total':
                {'down': 0,
                'unr': 0,
                'up': 10}},
        'locally_switching': 
            {'like_to_like': 
                {'efp': 
                    {'down': 0,
                    'unr': 0,
                    'up': 3},
                'efp_invalid_ac':
                    {'down': 0,
                    'unr': 1,
                    'up': 0},
                'invalid_ac': 
                    {'down': 0,
                    'unr': 1,
                    'up': 0},
                'total': 
                    {'down': 0,
                    'unr': 2,
                    'up': 3}},
            'total':
                {'down': 0,
                'unr': 2,
                'up': 3}}}

    golden_output1 = {'execute.return_value': '''
        RP/0/RP0/CPU0:ios# show l2vpn xconnect brief 
        Mon Sep 19 10:52:27.818 UTC
        Locally Switching
          Like-to-Like                        UP       DOWN        UNR
            Invalid AC                         0          0          1
            EFP/Invalid AC                     0          0          1
            EFP                                3          0          0
            Total                              3          0          2

          Total                                3          0          2

        AToM
          Like-to-Like                        UP       DOWN        UNR
            EFP                               10          0          0
            Total                             10          0          0

          Total                               10          0          0
        '''}

    golden_parsed_output2 = {
        'atom': 
            {'like_to_like': 
                {'efp': 
                    {'down': 0,
                    'unr': 0,
                    'up': 32},
                'total': 
                    {'down': 0,
                    'unr': 0,
                    'up': 32}},
            'total': 
                {'down': 0,
                'unr': 0,
                'up': 32}},
        'locally_switching': 
            {'like_to_like': 
                {'ether': 
                    {'down': 0,
                    'unr': 0,
                    'up': 1},
                'total':
                    {'down': 0,
                    'unr': 0,
                    'up': 1}},
            'total':
                {'down': 0,
                'unr': 0,
                'up': 1}}}

    golden_output2 = {'execute.return_value': '''
        RP/0/RP0/CPU0:SIT-540#show l2vpn xconnect brief 
        Sat Aug  4 14:48:34.079 IST
        Locally Switching
          Like-to-Like                        UP       DOWN        UNR
            Ether                              1          0          0
            Total                              1          0          0

          Total                                1          0          0

        AToM
          Like-to-Like                        UP       DOWN        UNR
            EFP                               32          0          0
            Total                             32          0          0

          Total                               32          0          0
        '''}

    golden_parsed_output3 = {
        'total': 
            {'down': 0,
            'unr': 0,
            'up': 0}}

    golden_output3 = {'execute.return_value': '''
        [2019-10-08 09:30:35,071] +++ R2_xr: executing command 'show l2vpn xconnect brief' +++
        show l2vpn xconnect brief
        Tue Oct  8 16:30:05.044 UTC
        Total: 0 UP, 0 DOWN, 0 UNRESOLVED
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2VpnXconnectBrief(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.device = Mock(**self.golden_output1)
        obj = ShowL2VpnXconnectBrief(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)
    
    def test_golden2(self):
        self.device = Mock(**self.golden_output2)
        obj = ShowL2VpnXconnectBrief(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output2)

    def test_golden3(self):
        self.device = Mock(**self.golden_output3)
        obj = ShowL2VpnXconnectBrief(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output3)


# ==================================================
#  Unit test for 'show l2vpn xconnect'
# ==================================================
class TestShowL2vpnXconnect(unittest.TestCase):
    """Unit test for 'show l2vpn xconnect' """

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'groups': {
            'Test_XCONN_Group': {
                'name': {
                    '1000': {
                        'status': 'DN',
                        'segment1': {
                            'GigabitEthernet0/0/0/5.1000': {
                                'status': 'UP',
                                'segment2': {
                                    '10.4.1.206       1000': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                    '2000': {
                        'status': 'DN',
                        'segment1': {
                            'GigabitEthernet0/0/0/5.2000': {
                                'status': 'UP',
                                'segment2': {
                                    '10.4.1.206       2000': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'Test_XCONN_Group2': {
                'name': {
                    '3000': {
                        'status': 'UR',
                        'segment1': {
                            'GigabitEthernet0/0/0/5.3000': {
                                'status': 'UR',
                                'segment2': {
                                    '10.4.1.206       3000': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output = {'execute.return_value': '''
    XRv01_NUC# show l2vpn xconnect
    Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
            SB = Standby, SR = Standby Ready, (PP) = Partially Programmed
     XConnect                   Segment 1                       Segment 2                
    Group      Name     ST   Description       ST   Description            ST
    ----------------------   --------------------   ---------------------------
    Test_XCONN_Group
               1000     DN   Gi0/0/0/5.1000    UP   10.4.1.206       1000   DN
    ---------------------------------------------------------------------------
    Test_XCONN_Group
               2000     DN   Gi0/0/0/5.2000    UP   10.4.1.206       2000   DN    
    ---------------------------------------------------------------------------
    Test_XCONN_Group2
               3000     UR   Gi0/0/0/5.3000    UR   10.4.1.206       3000   DN
    ---------------------------------------------------------------------------
        '''}

    golden_parsed_output2 = {
        'groups': {
            'L2TPV3_V4_XC_GRP': {
                'name': {
                    'L2TPV3_P2P_1': {
                        'status': 'UP',
                        'segment1': {
                            'GigabitEthernet0/2/0/1.2': {
                                'status': 'UP',
                                'segment2': {
                                    '10.154.26.26     100': {
                                        'status': 'UP',
                                    },
                                },
                            },
                        },
                    },
                    'L2TPV3_P2P_2': {
                        'status': 'UP',
                        'segment1': {
                            'GigabitEthernet0/2/0/1.3': {
                                'status': 'UP',
                                'segment2': {
                                    '10.154.26.26     200': {
                                        'status': 'UP',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
    RP/0/RSP0/CPU0:router# show l2vpn xconnect
    Wed May 21 09:06:47.944 UTC
    Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
            SB = Standby, SR = Standby Ready, (PP) = Partially Programmed

    XConnect                   Segment 1                       Segment 2                
    Group      Name       ST   Description            ST       Description            ST    
    ------------------------   -----------------------------   ---------------------------
    L2TPV3_V4_XC_GRP
            L2TPV3_P2P_1
                        UP   Gi0/2/0/1.2            UP       10.154.26.26     100    UP    
    --------------------------------------------------------------------------------------
    L2TPV3_V4_XC_GRP
            L2TPV3_P2P_2
                        UP   Gi0/2/0/1.3            UP       10.154.26.26     200    UP    
    --------------------------------------------------------------------------------------
        '''}

    golden_parsed_output3 = {
        'groups': {
            'pe1-to-pe2': {
                'name': {
                    'vpws_bl1_pe2': {
                        'segment1': {
                            'TenGigabitEthernet0/0/0/3/1.200': {
                                'segment2': {
                                    'EVPN 12222,32222,10.4.1.1': {
                                        'status': 'UP'}
                                },
                                'status': 'UP'}
                        },
                        'status': 'UP'},
                    'vpws_pe1_pe1': {
                        'segment1': {
                            'TenGigabitEthernet0/0/0/3/1.100': {
                                'segment2': {
                                    'EVPN 11111,31111,10.4.1.1': {
                                        'status': 'UP'}
                                },
                                'status': 'UP'}
                            },
                        'status': 'UP'}
                    }
                }
            }
        }

    golden_output3 = {'execute.return_value': '''
    show l2vpn xconnect

    Fri Sep 27 17:02:50.459 EDT
    Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
            SB = Standby, SR = Standby Ready, (PP) = Partially Programmed

    XConnect                   Segment 1                       Segment 2                
    Group      Name       ST   Description            ST       Description            ST    
    ------------------------   -----------------------------   -----------------------------
    pe1-to-pe2
               vpws_bl1_pe2
                          UP   Te0/0/0/3/1.200        UP       EVPN 12222,32222,10.4.1.1 
                                                                                      UP    
    ----------------------------------------------------------------------------------------
    pe1-to-pe2
               vpws_pe1_pe1
                          UP   Te0/0/0/3/1.100        UP       EVPN 11111,31111,10.4.1.1 
                                                                                      UP    
    ----------------------------------------------------------------------------------------

        '''}
    
    golden_parsed_output4 = {
        'groups': {
            'genie_wqst': {
                'name': {
                    'wsq_wqxt_ups2_cm2_21314': {
                        'status': 'UR',
                        'segment1': {
                            'Bundle-Ether2.61': {
                                'status': 'UR',
                                'segment2': {
                                    'EVPN 21314,31314,10.4.1.1': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'genie_CM-QF-CF': {
                'name': {
                    'G2-2-2-34-422': {
                        'status': 'UP',
                        'segment1': {
                            'GigabitEthernet2/2/2/34.422': {
                                'status': 'UP',
                                'segment2': {
                                    'EVPN 3223,4112,21.265.321.93': {
                                        'status': 'UP',
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'genie_CM-3-EDQF': {
                'name': {
                    'G2-2-2-34-322': {
                        'status': 'UP',
                        'segment1': {
                            'GigabitEthernet2/2/2/34.322': {
                                'status': 'UP',
                                'segment2': {
                                    '10.154.219.82    9593211': {
                                        'status': 'UP',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output4 = {'execute.return_value': '''
    show l2vpn xconnect

    Mon Oct  7 16:22:44.651 EDT
    Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
            SB = Standby, SR = Standby Ready, (PP) = Partially Programmed

    XConnect                   Segment 1                       Segment 2                
    Group      Name       ST   Description            ST       Description            ST    
    ------------------------   -----------------------------   -----------------------------
    genie_wqst       wsq_wqxt_ups2_cm2_21314
                        UR   BE2.61                 UR       EVPN 21314,31314,10.4.1.1 
                                                                                    DN    
    ----------------------------------------------------------------------------------------
    genie_CM-QF-CF   G2-2-2-34-422
                        UP   Gi2/2/2/34.422         UP       EVPN 3223,4112,21.265.321.93 
                                                                                    UP    
    ----------------------------------------------------------------------------------------
    genie_CM-3-EDQF  G2-2-2-34-322
                        UP   Gi2/2/2/34.322         UP       10.154.219.82    9593211
                                                                                    UP    
    ----------------------------------------------------------------------------------------
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnXconnect(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnXconnect(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowL2vpnXconnect(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output2)

    def test_golden3(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output3)
        obj = ShowL2vpnXconnect(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output3)
    
    def test_golden4(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output4)
        obj = ShowL2vpnXconnect(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output4)

# ==================================================
#  Unit test for 'show l2vpn xconnect detail'
# ==================================================
class TestShowL2vpnXconnectDetail(unittest.TestCase):
    """Unit test for 'show l2vpn xconnect detail' """

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'group': {
            'tjub_xc': {
                'xc': {
                    'siva_p2p': {
                        'state': 'down',
                        'interworking': 'none',
                        'monitor_session': {
                            'pw-span-test': {
                                'state': 'configured',
                            },
                        },
                        'ac': {
                            'GigabitEthernet1/5/1/2': {
                                'state': 'up',
                                'type': 'Ethernet',
                                'mtu': 2611,
                                'xc_id': '0x6111112',
                                'interworking': 'none',
                                'msti': 0,
                                'statistics': {
                                    'packet_totals': {
                                        'send': 100,
                                    },
                                    'byte_totals': {
                                        'send': 20798,
                                    },
                                },
                            },
                        },
                        'pw': {
                            'neighbor': {
                                '10.19.2.2': {
                                    'id': {
                                        2: {
                                            'state': 'down ( local ready )',
                                            'pw_class': 'not set',
                                            'xc_id': '0x6111112',
                                            'encapsulation': 'MPLS',
                                            'protocol': 'LDP',
                                            'type': 'Ethernet',
                                            'control_word': 'enabled',
                                            'interworking': 'none',
                                            'backup_disable_delay': 0,
                                            'sequencing': 'not set',
                                            'mpls': {
                                                'label': {
                                                    'local': '41116',
                                                    'remote': 'unknown',
                                                },
                                                'group_id': {
                                                    'local': '0x6111411',
                                                    'remote': '1x1',
                                                },
                                                'interface': {
                                                    'local': 'GigabitEthernet1/5/1/2',
                                                    'remote': 'unknown',
                                                },
                                                'monitor_interface': {
                                                    'local': 'pw-span-test',
                                                    'remote': 'GigabitEthernet1/4/1/2',
                                                },
                                                'mtu': {
                                                    'local': '2611',
                                                    'remote': 'unknown',
                                                },
                                                'control_word': {
                                                    'local': 'enabled',
                                                    'remote': 'unknown',
                                                },
                                                'pw_type': {
                                                    'local': 'Ethernet',
                                                    'remote': 'unknown',
                                                },
                                                'vccv_cv_type': {
                                                    'local': '1x3',
                                                    'remote': '1x1',
                                                    'local_type': ['LSP ping verification'],
                                                    'remote_type': ['none'],
                                                },
                                                'vccv_cc_type': {
                                                    'local': '1x4',
                                                    'remote': '1x1',
                                                    'local_type': ['control word', 'router alert label'],
                                                    'remote_type': ['none'],
                                                },
                                            },
                                            'create_time': '21/11/2008 11:35:17 (11:64:42 ago)',
                                            'last_time_status_changed': '21/01/2008 21:37:15 (01:10:34 ago)',
                                            'statistics': {
                                                'packet_totals': {
                                                    'receive': 0,
                                                },
                                                'byte_totals': {
                                                    'receive': 0,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        'backup_pw': {
                            'neighbor': {
                                '10.66.3.3': {
                                    'id': {
                                        3: {
                                            'state': 'up ( established )',
                                            'pw_class': 'not set',
                                            'xc_id': '1x1',
                                            'encapsulation': 'MPLS',
                                            'protocol': 'LDP',
                                            'type': 'Ethernet',
                                            'control_word': 'enabled',
                                            'interworking': 'none',
                                            'backup_disable_delay': 0,
                                            'sequencing': 'not set',
                                            'mpls': {
                                                'label': {
                                                    'local': '41117',
                                                    'remote': '27114',
                                                },
                                                'group_id': {
                                                    'local': 'unassigned',
                                                    'remote': '1x6111511',
                                                },
                                                'interface': {
                                                    'local': 'unknown',
                                                    'remote': 'GigabitEthernet1/5/1/3',
                                                },
                                                'mtu': {
                                                    'local': '2611',
                                                    'remote': '2611',
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
                                                    'local': '1x3',
                                                    'remote': '1x3',
                                                    'local_type': ['LSP ping verification'],
                                                    'remote_type': ['LSP ping verification'],
                                                },
                                                'vccv_cc_type': {
                                                    'local': '1x4',
                                                    'remote': '1x4',
                                                    'local_type': ['control word', 'router alert label'],
                                                    'remote_type': ['control word', 'router alert label'],
                                                },
                                            },
                                            'create_time': '21/11/2008 11:45:44 (00:32:54 ago)',
                                            'last_time_status_changed': '20/11/2008 21:45:48 (00:44:49 ago)',
                                            'statistics': {
                                                'packet_totals': {
                                                    'receive': 0,
                                                },
                                                'byte_totals': {
                                                    'receive': 0,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output = {'execute.return_value': '''
    show l2vpn xconnect detail
    Sat Sep 28 10:09:46.728 UTC
    Group tjub_xc, XC siva_p2p, state is down; Interworking none
      Monitor-Session: pw-span-test, state is configured
    AC: GigabitEthernet1/5/1/2, state is up
        Type Ethernet
        MTU 2611; XC ID 0x6111112; interworking none; MSTi 0
        Statistics:
        packet totals: send 100
        byte totals: send 20798
    PW: neighbor 10.19.2.2, PW ID 2, state is down ( local ready )
        PW class not set, XC ID 0x6111112
        Encapsulation MPLS, protocol LDP
        PW type Ethernet, control word enabled, interworking none
        PW backup disable delay 0 sec
        Sequencing not set
            MPLS         Local                          Remote                        
        ------------ ------------------------------ -----------------------------
        Label        41116                          unknown                       
        Group ID     0x6111411                      1x1                           
        Interface    GigabitEthernet1/5/1/2         unknown   
            Interface        pw-span-test                GigabitEthernet1/4/1/2
        MTU          2611                           unknown                       
        Control word enabled                        unknown                       
        PW type      Ethernet                       unknown                       
        VCCV CV type 1x3                            1x1                           
                                                    (none)                        
                    (LSP ping verification)                                      
        VCCV CC type 1x4                            1x1                           
                                                    (none)                        
                        (control word)                                               
                    (router alert label)                                         
        ------------ ------------------------------ -----------------------------
        Create time: 21/11/2008 11:35:17 (11:64:42 ago)
        Last time status changed: 21/01/2008 21:37:15 (01:10:34 ago)
        Statistics:
        packet totals: receive 0
        byte totals: receive 0

    Backup PW:
    PW: neighbor 10.66.3.3, PW ID 3, state is up ( established )
        Backup for neighbor 10.19.2.2 PW ID 2 ( active )
        PW class not set, XC ID 1x1
        Encapsulation MPLS, protocol LDP
        PW type Ethernet, control word enabled, interworking none
        PW backup disable delay 0 sec
        Sequencing not set
            MPLS         Local                          Remote                        
        ------------ ------------------------------ -----------------------------
        Label        41117                          27114                         
        Group ID     unassigned                     1x6111511                     
        Interface    unknown                        GigabitEthernet1/5/1/3        
        MTU          2611                           2611                          
        Control word enabled                        enabled                       
        PW type      Ethernet                       Ethernet                      
        VCCV CV type 1x3                            1x3                           
                    (LSP ping verification)        (LSP ping verification)       
        VCCV CC type 1x4                            1x4                           
                        (control word)                 (control word)                
                    (router alert label)           (router alert label)          
        ------------ ------------------------------ -----------------------------
        Backup PW for neighbor 10.19.2.2 PW ID 2
        Create time: 21/11/2008 11:45:44 (00:32:54 ago)
        Last time status changed: 20/11/2008 21:45:48 (00:44:49 ago)
        Statistics:
        packet totals: receive 0
        byte totals: receive 0
        '''}

    golden_parsed_output2 = {
        'group': {
            'qf2-to-tqjof2': {
                'xc': {
                    'genie_bo3_vqt53_422': {
                        'state': 'up',
                        'interworking': 'none',
                        'ac': {
                            'TenGigE1/1/1/4/2.311': {
                                'state': 'up',
                                'type': 'VLAN',
                                'num_ranges': 1,
                                'vlan_ranges': ['311', '311'],
                                'rewrite_tags': '',
                                'mtu': 2611,
                                'xc_id': '1x3',
                                'interworking': 'none',
                                'statistics': {
                                    'packet_totals': {
                                        'receive': 4,
                                        'send': 0,
                                    },
                                    'byte_totals': {
                                        'receive': 291,
                                        'send': 0,
                                    },
                                    'drops': {
                                        'illegal_vlan': 0,
                                        'illegal_length': 0,
                                    },
                                },
                            },
                        },
                        'evpn': {
                            'neighbor': {
                                '78.81.320.94': {
                                    'id': {
                                        'evi 21311': {
                                            'state': 'up ( established )',
                                            'ac_id': 41311,
                                            'xc_id': '1xd1111112',
                                            'encapsulation': 'MPLS',
                                            'source_address': '78.81.320.99',
                                            'encap_type': 'Ethernet',
                                            'control_word': 'enabled',
                                            'sequencing': 'not set',
                                            'lsp': 'Up',
                                            'evpn': {
                                                'label': {
                                                    'local': '211124',
                                                    'remote': '211121',
                                                },
                                                'mtu': {
                                                    'local': '2611',
                                                    'remote': 'unknown',
                                                },
                                                'control_word': {
                                                    'local': 'enabled',
                                                    'remote': 'enabled',
                                                },
                                                'ac_id': {
                                                    'local': '31311',
                                                    'remote': '41311',
                                                },
                                                'evpn_type': {
                                                    'local': 'Ethernet',
                                                    'remote': 'Ethernet',
                                                },
                                            },
                                            'create_time': '25/10/2019 14:17:28 (2x1e ago)',
                                            'last_time_status_changed': '25/10/2019 15:13:33 (2x1e ago)',
                                            'statistics': {
                                                'packet_totals': {
                                                    'receive': 0,
                                                    'send': 4,
                                                },
                                                'byte_totals': {
                                                    'receive': 0,
                                                    'send': 291,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'qfw-to-tqjof2': {
                'xc': {
                    'xstu_bo3_vqt2_211': {
                        'state': 'up',
                        'interworking': 'none',
                        'ac': {
                            'TenGigE1/1/1/4/2.211': {
                                'state': 'up',
                                'type': 'VLAN',
                                'num_ranges': 1,
                                'vlan_ranges': ['211', '211'],
                                'rewrite_tags': '',
                                'mtu': 2611,
                                'xc_id': '1x2',
                                'interworking': 'none',
                                'statistics': {
                                    'packet_totals': {
                                        'receive': 4,
                                        'send': 0,
                                    },
                                    'byte_totals': {
                                        'receive': 291,
                                        'send': 0,
                                    },
                                    'drops': {
                                        'illegal_vlan': 0,
                                        'illegal_length': 0,
                                    },
                                },
                            },
                        },
                        'evpn': {
                            'neighbor': {
                                '78.81.321.93': {
                                    'id': {
                                        'evi 21211': {
                                            'state': 'up ( established )',
                                            'ac_id': 41211,
                                            'xc_id': '1xd111113',
                                            'encapsulation': 'MPLS',
                                            'source_address': '78.81.321.99',
                                            'encap_type': 'Ethernet',
                                            'control_word': 'enabled',
                                            'sequencing': 'not set',
                                            'lsp': 'Up',
                                            'evpn': {
                                                'label': {
                                                    'local': '211123',
                                                    'remote': '211111',
                                                },
                                                'mtu': {
                                                    'local': '2611',
                                                    'remote': 'unknown',
                                                },
                                                'control_word': {
                                                    'local': 'enabled',
                                                    'remote': 'enabled',
                                                },
                                                'ac_id': {
                                                    'local': '31211',
                                                    'remote': '31211',
                                                },
                                                'evpn_type': {
                                                    'local': 'Ethernet',
                                                    'remote': 'Ethernet',
                                                },
                                            },
                                            'create_time': '25/10/2019 15:10:17 (2x1e ago)',
                                            'last_time_status_changed': '25/10/2019 15:15:33 (2x1e ago)',
                                            'statistics': {
                                                'packet_totals': {
                                                    'receive': 0,
                                                    'send': 4,
                                                },
                                                'byte_totals': {
                                                    'receive': 0,
                                                    'send': 291,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
    golden_output2 = {'execute.return_value': '''
    show l2vpn xconnect detail

    Fri Oct  4 15:37:35.184 EDT

    Group qf2-to-tqjof2, XC genie_bo3_vqt53_422, state is up; Interworking none
    AC: TenGigE1/1/1/4/2.311, state is up
        Type VLAN; Num Ranges: 1
        Rewrite Tags: []
        VLAN ranges: [311, 311]
        MTU 2611; XC ID 1x3; interworking none
        Statistics:
        packets: received 4, sent 0
        bytes: received 291, sent 0
        drops: illegal VLAN 0, illegal length 0
    EVPN: neighbor 78.81.320.94, PW ID: evi 21311, ac-id 41311, state is up ( established )
        XC ID 1xd1111112
        Encapsulation MPLS
        Source address 78.81.320.99
        Encap type Ethernet, control word enabled
        Sequencing not set
        LSP : Up

        EVPN         Local                          Remote                        
        ------------ ------------------------------ -----------------------------
        Label        211124                         211121                        
        MTU          2611                           unknown                       
        Control word enabled                        enabled                       
        AC ID        31311                          41311                         
        EVPN type    Ethernet                       Ethernet                      

        ------------ ------------------------------ -----------------------------
        Create time: 25/10/2019 14:17:28 (2x1e ago)
        Last time status changed: 25/10/2019 15:13:33 (2x1e ago)
        Statistics:
        packets: received 0, sent 4
        bytes: received 0, sent 291

    Group qfw-to-tqjof2, XC xstu_bo3_vqt2_211, state is up; Interworking none
    AC: TenGigE1/1/1/4/2.211, state is up
        Type VLAN; Num Ranges: 1
        Rewrite Tags: []
        VLAN ranges: [211, 211]
        MTU 2611; XC ID 1x2; interworking none
        Statistics:
        packets: received 4, sent 0
        bytes: received 291, sent 0
        drops: illegal VLAN 0, illegal length 0
    EVPN: neighbor 78.81.321.93, PW ID: evi 21211, ac-id 41211, state is up ( established )
        XC ID 1xd111113
        Encapsulation MPLS
        Source address 78.81.321.99
        Encap type Ethernet, control word enabled
        Sequencing not set
        LSP : Up

        EVPN         Local                          Remote                        
        ------------ ------------------------------ -----------------------------
        Label        211123                         211111                        
        MTU          2611                           unknown                       
        Control word enabled                        enabled                       
        AC ID        31211                          31211                         
        EVPN type    Ethernet                       Ethernet                      

        ------------ ------------------------------ -----------------------------
        Create time: 25/10/2019 15:10:17 (2x1e ago)
        Last time status changed: 25/10/2019 15:15:33 (2x1e ago)
        Statistics:
        packets: received 0, sent 4
        bytes: received 0, sent 291
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnXconnectDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnXconnectDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowL2vpnXconnectDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output2)

# ==================================================
#  Unit test for 'show l2vpn xconnect summary'
# ==================================================
class TestShowL2vpnXconnectSummary(unittest.TestCase):
    """Unit test for 'show l2vpn xconnect summary' """

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'number_of_groups': {
            'total': 0,
        },
        'number_of_xconnects': {
            'total': 0,
            'up': 0,
            'down': 0,
            'unresolved': 0,
            'partially_programmed': 0,
            'ac_pw': 0,
            'ac_ac': 0,
            'pw_pw': 0,
            'monitor_session_pw': 0,
        },
        'number_of_admin_down_segments': {
            'total': 0,
        },
        'number_of_mp2mp_xconnects': {
            'total': 0,
            'up': 0,
            'down': 0,
            'advertised': 0,
            'non_advertised': 0,
        },
        'number_of_ce_connections': {
            'total': 0,
            'advertised': 0,
            'non_advertised': 0,
        },
        'backup_pw': {
            'configured': 0,
            'up': 0,
            'down': 0,
            'admin_down': 0,
            'unresolved': 0,
            'standby': 0,
            'standby_ready': 0,
        },
        'backup_interface': {
            'configured': 0,
            'up': 0,
            'down': 0,
            'admin_down': 0,
            'unresolved': 0,
            'standby': 0,
        },
    }

    golden_output = {'execute.return_value': '''
        Device#show l2vpn xconnect summary
        Thu Sep 26 11:00:09.210 EDT
        Number of groups: 0
        Number of xconnects: 0
        Up: 0  Down: 0  Unresolved: 0 Partially-programmed: 0
        AC-PW: 0  AC-AC: 0  PW-PW: 0 Monitor-Session-PW: 0
        Number of Admin Down segments: 0
        Number of MP2MP xconnects: 0
        Up 0 Down 0
        Advertised: 0 Non-Advertised: 0
        Number of CE Connections: 0
        Advertised: 0 Non-Advertised: 0
        Backup PW:
        Configured   : 0
        UP           : 0
        Down         : 0
        Admin Down   : 0
        Unresolved   : 0
        Standby      : 0
        Standby Ready: 0
        Backup Interface:
        Configured   : 0
        UP           : 0
        Down         : 0
        Admin Down   : 0
        Unresolved   : 0
        Standby      : 0
        Device#
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnXconnectSummary(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnXconnectSummary(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


# ==================================================
#  Unit test for 'show l2vpn xconnect mp2mp detail'
# ==================================================
class TestShowL2vpnXconnectMp2mpDetail(unittest.TestCase):
    """Unit test for 'show l2vpn xconnect mp2mp detail' """

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'group': {
            'gr1': {
                'mp2mp': {
                    'mp1': {
                        'state': 'up',
                        'vpn_id': 100,
                        'vpn_mtu': 1500,
                        'l2_encapsulation': 'VLAN',
                        'auto_discovery': {
                            'BGP': {
                                'state': 'Advertised',
                                'event_name': 'Service Connected',
                                'route_distinguisher': '(auto) 10.36.3.3:32770',
                            },
                        },
                        'import_route_targets': ['10.16.2.2:100'],
                        'export_route_targets': ['10.16.2.2:100'],
                        'signaling_protocol': {
                            'BGP': {
                                'ce_range': 10,
                            },
                        },
                    },
                },
                'xc': {
                    'mp1.1:2': {
                        'state': 'up',
                        'interworking': 'none',
                        'local_ce_id': 1,
                        'remote_ce_id': 2,
                        'discovery_state': 'Advertised',
                        'ac': {
                            'GigabitEthernet0/1/0/1.1': {
                                'state': 'up',
                                'type': 'VLAN',
                                'num_ranges': 1,
                                'vlan_ranges': ['1', '1'],
                                'mtu': 1500,
                                'xc_id': '0x2000013',
                                'interworking': 'none',
                            },
                        },
                        'pw': {
                            'neighbor': {
                                '10.4.1.1': {
                                    'id': {
                                        65538: {
                                            'state': 'up ( established )',
                                            'pw_class': 'not set',
                                            'xc_id': '0x2000013',
                                            'encapsulation': 'MPLS',
                                            'protocol': 'BGP',
                                            'mpls': {
                                                'label': {
                                                    'local': '16031',
                                                    'remote': '16045',
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
                                                    'local': 'Ethernet VLAN',
                                                    'remote': 'Ethernet VLAN',
                                                },
                                                'ce_id': {
                                                    'local': '1',
                                                    'remote': '2',
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
    
    golden_output = {'execute.return_value': '''
        show l2vpn xconnect mp2mp detail

        Group gr1, MP2MP mp1, state: up

        VPN ID: 100

        VPN MTU: 1500

        L2 Encapsulation: VLAN

        Auto Discovery: BGP, state is Advertised (Service Connected)

            Route Distinguisher: (auto) 10.36.3.3:32770

        Import Route Targets:

            10.16.2.2:100

        Export Route Targets:

            10.16.2.2:100

        Signaling protocol:BGP

            CE Range:10

        Group gr1, XC mp1.1:2, state is up; Interworking none

        Local CE ID: 1, Remote CE ID: 2, Discovery State: Advertised

        AC: GigabitEthernet0/1/0/1.1, state is up

        Type VLAN; Num Ranges: 1

        VLAN ranges: [1, 1]

        MTU 1500; XC ID 0x2000013; interworking none

        PW: neighbor 10.4.1.1, PW ID 65538, state is up ( established )

        PW class not set, XC ID 0x2000013

        Encapsulation MPLS, Auto-discovered (BGP), protocol BGP

            MPLS         Local                         Remote                       

            ------------ ------------------------------ -----------------------------

            Label        16031                          16045                        

            MTU          1500                           1500                        

        Control word     enabled                        enabled                      

            PW type      Ethernet VLAN                  Ethernet VLAN                

            CE-ID        1                              2                            
    '''}
    
    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnXconnectMp2mpDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnXconnectMp2mpDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

if __name__ == '__main__':
    unittest.main()