# border2-dc1

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [DNS Domain](#dns-domain)
  - [IP Name Servers](#ip-name-servers)
  - [NTP](#ntp)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [AAA Authorization](#aaa-authorization)
- [Monitoring](#monitoring)
  - [TerminAttr Daemon](#terminattr-daemon)
- [MLAG](#mlag)
  - [MLAG Summary](#mlag-summary)
  - [MLAG Device Configuration](#mlag-device-configuration)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
- [VLANs](#vlans)
  - [VLANs Summary](#vlans-summary)
  - [VLANs Device Configuration](#vlans-device-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Port-Channel Interfaces](#port-channel-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
  - [VLAN Interfaces](#vlan-interfaces)
  - [VXLAN Interface](#vxlan-interface)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [Virtual Router MAC Address](#virtual-router-mac-address)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [EOS CLI Device Configuration](#eos-cli-device-configuration)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management0 | oob_management | oob | MGMT | 192.168.66.102/24 | 192.168.66.1 |

##### IPv6

| Management Interface | Description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management0 | oob_management | oob | MGMT | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management0
   description oob_management
   no shutdown
   vrf MGMT
   ip address 192.168.66.102/24
```

### DNS Domain

DNS domain: fun.aristanetworks.com

#### DNS Domain Device Configuration

```eos
dns domain fun.aristanetworks.com
!
```

### IP Name Servers

#### IP Name Servers Summary

| Name Server | VRF | Priority |
| ----------- | --- | -------- |
| 10.14.0.1 | MGMT | - |

#### IP Name Servers Device Configuration

```eos
ip name-server vrf MGMT 10.14.0.1
```

### NTP

#### NTP Summary

##### NTP Local Interface

| Interface | VRF |
| --------- | --- |
| Management0 | MGMT |

##### NTP Servers

| Server | VRF | Preferred | Burst | iBurst | Version | Min Poll | Max Poll | Local-interface | Key |
| ------ | --- | --------- | ----- | ------ | ------- | -------- | -------- | --------------- | --- |
| 1.pool.ntp.org | MGMT | True | - | True | - | - | - | - | - |

#### NTP Device Configuration

```eos
!
ntp local-interface vrf MGMT Management0
ntp server vrf MGMT 1.pool.ntp.org prefer iburst
```

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

#### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

#### Management API HTTP Device Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

## Authentication

### Local Users

#### Local Users Summary

| User | Privilege | Role | Disabled | Shell |
| ---- | --------- | ---- | -------- | ----- |
| admin | 15 | network-admin | False | - |
| cvpadmin | 15 | network-admin | False | - |

#### Local Users Device Configuration

```eos
!
username admin privilege 15 role network-admin secret sha512 <removed>
username cvpadmin privilege 15 role network-admin secret sha512 <removed>
```

### AAA Authorization

#### AAA Authorization Summary

| Type | User Stores |
| ---- | ----------- |
| Exec | local |

Authorization for configuration commands is disabled.

#### AAA Authorization Device Configuration

```eos
aaa authorization exec default local
!
```

## Monitoring

### TerminAttr Daemon

#### TerminAttr Daemon Summary

| CV Compression | CloudVision Servers | VRF | Authentication | Smash Excludes | Ingest Exclude | Bypass AAA |
| -------------- | ------------------- | --- | -------------- | -------------- | -------------- | ---------- |
| gzip | avd-cv-master-1.fun.aristanetworks.com:9910 | MGMT | token,/mnt/flash/token | ale,flexCounter,hardware,kni,pulse,strata | /Sysdb/cell/1/agent,/Sysdb/cell/2/agent | False |

#### TerminAttr Daemon Device Configuration

```eos
!
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=avd-cv-master-1.fun.aristanetworks.com:9910 -cvauth=token,/mnt/flash/token -cvvrf=MGMT -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -taillogs
   no shutdown
```

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| BORDERS_DC1 | Vlan4094 | 10.100.3.0 | Port-Channel5 |

Dual primary detection is disabled.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id BORDERS_DC1
   local-interface Vlan4094
   peer-address 10.100.3.0
   peer-link Port-Channel5
   reload-delay mlag 300
   reload-delay non-mlag 330
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **mstp**

#### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 16384 |

#### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4093-4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4093-4094
spanning-tree mst 0 priority 16384
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Device Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## VLANs

### VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 10 | guest_10 | - |
| 20 | data_20 | - |
| 3009 | MLAG_iBGP_guest | LEAF_PEER_L3 |
| 3019 | MLAG_iBGP_data | LEAF_PEER_L3 |
| 4093 | LEAF_PEER_L3 | LEAF_PEER_L3 |
| 4094 | MLAG_PEER | MLAG |

### VLANs Device Configuration

```eos
!
vlan 10
   name guest_10
!
vlan 20
   name data_20
!
vlan 3009
   name MLAG_iBGP_guest
   trunk group LEAF_PEER_L3
!
vlan 3019
   name MLAG_iBGP_data
   trunk group LEAF_PEER_L3
!
vlan 4093
   name LEAF_PEER_L3
   trunk group LEAF_PEER_L3
!
vlan 4094
   name MLAG_PEER
   trunk group MLAG
```

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet5 | MLAG_PEER_border1-dc1_Ethernet5 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 5 |
| Ethernet6 | MLAG_PEER_border1-dc1_Ethernet6 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 5 |

*Inherited from Port-Channel Interface

##### Encapsulation Dot1q Interfaces

| Interface | Description | Type | Vlan ID | Dot1q VLAN Tag |
| --------- | ----------- | -----| ------- | -------------- |
| Ethernet3.10 | P2P_LINK_TO_WAN1-DC1_Ethernet2.10_vrf_guest | l3dot1q | - | 10 |
| Ethernet3.20 | P2P_LINK_TO_WAN1-DC1_Ethernet2.20_vrf_data | l3dot1q | - | 20 |
| Ethernet4.10 | P2P_LINK_TO_WAN2-DC1_Ethernet2.10_vrf_guest | l3dot1q | - | 10 |
| Ethernet4.20 | P2P_LINK_TO_WAN2-DC1_Ethernet2.20_vrf_data | l3dot1q | - | 20 |

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_SPINE1-DC1_Ethernet2 | routed | - | 10.100.0.5/31 | default | 9214 | False | - | - |
| Ethernet2 | P2P_LINK_TO_SPINE2-DC1_Ethernet2 | routed | - | 10.100.0.7/31 | default | 9214 | False | - | - |
| Ethernet3 | P2P_LINK_TO_WAN1-DC1_Ethernet2 | routed | - | 10.100.0.130/31 | default | 9214 | False | - | - |
| Ethernet3.10 | P2P_LINK_TO_WAN1-DC1_Ethernet2.10_vrf_guest | l3dot1q | - | 10.100.0.130/31 | guest | 9214 | False | - | - |
| Ethernet3.20 | P2P_LINK_TO_WAN1-DC1_Ethernet2.20_vrf_data | l3dot1q | - | 10.100.0.130/31 | data | 9214 | False | - | - |
| Ethernet4 | P2P_LINK_TO_WAN2-DC1_Ethernet2 | routed | - | 10.100.0.134/31 | default | 9214 | False | - | - |
| Ethernet4.10 | P2P_LINK_TO_WAN2-DC1_Ethernet2.10_vrf_guest | l3dot1q | - | 10.100.0.134/31 | guest | 9214 | False | - | - |
| Ethernet4.20 | P2P_LINK_TO_WAN2-DC1_Ethernet2.20_vrf_data | l3dot1q | - | 10.100.0.134/31 | data | 9214 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_SPINE1-DC1_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ip address 10.100.0.5/31
!
interface Ethernet2
   description P2P_LINK_TO_SPINE2-DC1_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ip address 10.100.0.7/31
!
interface Ethernet3
   description P2P_LINK_TO_WAN1-DC1_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ip address 10.100.0.130/31
!
interface Ethernet3.10
   description P2P_LINK_TO_WAN1-DC1_Ethernet2.10_vrf_guest
   no shutdown
   mtu 9214
   encapsulation dot1q vlan 10
   vrf guest
   ip address 10.100.0.130/31
!
interface Ethernet3.20
   description P2P_LINK_TO_WAN1-DC1_Ethernet2.20_vrf_data
   no shutdown
   mtu 9214
   encapsulation dot1q vlan 20
   vrf data
   ip address 10.100.0.130/31
!
interface Ethernet4
   description P2P_LINK_TO_WAN2-DC1_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ip address 10.100.0.134/31
!
interface Ethernet4.10
   description P2P_LINK_TO_WAN2-DC1_Ethernet2.10_vrf_guest
   no shutdown
   mtu 9214
   encapsulation dot1q vlan 10
   vrf guest
   ip address 10.100.0.134/31
!
interface Ethernet4.20
   description P2P_LINK_TO_WAN2-DC1_Ethernet2.20_vrf_data
   no shutdown
   mtu 9214
   encapsulation dot1q vlan 20
   vrf data
   ip address 10.100.0.134/31
!
interface Ethernet5
   description MLAG_PEER_border1-dc1_Ethernet5
   no shutdown
   channel-group 5 mode active
!
interface Ethernet6
   description MLAG_PEER_border1-dc1_Ethernet6
   no shutdown
   channel-group 5 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel5 | MLAG_PEER_border1-dc1_Po5 | switched | trunk | - | - | ['LEAF_PEER_L3', 'MLAG'] | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel5
   description MLAG_PEER_border1-dc1_Po5
   no shutdown
   switchport
   switchport mode trunk
   switchport trunk group LEAF_PEER_L3
   switchport trunk group MLAG
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 10.100.1.4/32 |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | 10.100.2.3/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 10.100.1.4/32
!
interface Loopback1
   description VTEP_VXLAN_Tunnel_Source
   no shutdown
   ip address 10.100.2.3/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan10 | guest_10 | guest | - | False |
| Vlan20 | data_20 | data | - | False |
| Vlan3009 | MLAG_PEER_L3_iBGP: vrf guest | guest | 9214 | False |
| Vlan3019 | MLAG_PEER_L3_iBGP: vrf data | data | 9214 | False |
| Vlan4093 | MLAG_PEER_L3_PEERING | default | 9214 | False |
| Vlan4094 | MLAG_PEER | default | 9214 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | VRRP | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ---- | ------ | ------- |
| Vlan10 |  guest  |  -  |  10.200.10.1/24  |  -  |  -  |  -  |  -  |
| Vlan20 |  data  |  -  |  10.200.20.1/24  |  -  |  -  |  -  |  -  |
| Vlan3009 |  guest  |  10.100.4.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3019 |  data  |  10.100.4.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4093 |  default  |  10.100.4.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4094 |  default  |  10.100.3.1/31  |  -  |  -  |  -  |  -  |  -  |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan10
   description guest_10
   no shutdown
   vrf guest
   ip address virtual 10.200.10.1/24
!
interface Vlan20
   description data_20
   no shutdown
   vrf data
   ip address virtual 10.200.20.1/24
!
interface Vlan3009
   description MLAG_PEER_L3_iBGP: vrf guest
   no shutdown
   mtu 9214
   vrf guest
   ip address 10.100.4.1/31
!
interface Vlan3019
   description MLAG_PEER_L3_iBGP: vrf data
   no shutdown
   mtu 9214
   vrf data
   ip address 10.100.4.1/31
!
interface Vlan4093
   description MLAG_PEER_L3_PEERING
   no shutdown
   mtu 9214
   ip address 10.100.4.1/31
!
interface Vlan4094
   description MLAG_PEER
   no shutdown
   mtu 9214
   no autostate
   ip address 10.100.3.1/31
```

### VXLAN Interface

#### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback1 |
| UDP port | 4789 |
| EVPN MLAG Shared Router MAC | mlag-system-id |

##### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 10 | 10010 | - | - |
| 20 | 10020 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| data | 20 | - |
| guest | 10 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description border2-dc1_VTEP
   vxlan source-interface Loopback1
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 10 vni 10010
   vxlan vlan 20 vni 10020
   vxlan vrf data vni 20
   vxlan vrf guest vni 10
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### Virtual Router MAC Address

#### Virtual Router MAC Address Summary

Virtual Router MAC Address: 00:1c:73:00:dc:01

#### Virtual Router MAC Address Device Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:dc:01
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| data | True |
| guest | True |
| MGMT | False |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf data
ip routing vrf guest
no ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| data | false |
| guest | false |
| MGMT | false |

### Static Routes

#### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP | Exit interface | Administrative Distance | Tag | Route Name | Metric |
| --- | ------------------ | ----------- | -------------- | ----------------------- | --- | ---------- | ------ |
| MGMT | 0.0.0.0/0 | 192.168.66.1 | - | 1 | - | - | - |

#### Static Routes Device Configuration

```eos
!
ip route vrf MGMT 0.0.0.0/0 192.168.66.1
```

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65101 | 10.100.1.4 |

| BGP Tuning |
| ---------- |
| no bgp default ipv4-unicast |
| maximum-paths 4 ecmp 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

##### IPv4-UNDERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Send community | all |
| Maximum routes | 12000 |

##### MLAG-IPv4-UNDERLAY-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65101 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 12000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 10.100.0.4 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.0.6 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.0.131 | 65000 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.0.135 | 65000 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.1.1 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.100.1.2 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.100.4.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 10.100.0.131 | 65000 | data | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.0.135 | 65000 | data | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.4.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | data | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 10.100.0.131 | 65000 | guest | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.0.135 | 65000 | guest | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.100.4.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | guest | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| EVPN-OVERLAY-PEERS | True | default |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 10 | 10.100.1.4:10010 | 10010:10010 | - | - | learned |
| 20 | 10.100.1.4:10020 | 10020:10020 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute |
| --- | ------------------- | ------------ |
| data | 10.100.1.4:20 | connected |
| guest | 10.100.1.4:10 | connected |

#### Router BGP Device Configuration

```eos
!
router bgp 65101
   router-id 10.100.1.4
   maximum-paths 4 ecmp 4
   no bgp default ipv4-unicast
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER peer group
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65101
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description border1-dc1
   neighbor MLAG-IPv4-UNDERLAY-PEER send-community
   neighbor MLAG-IPv4-UNDERLAY-PEER maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER route-map RM-MLAG-PEER-IN in
   neighbor 10.100.0.4 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.100.0.4 remote-as 65100
   neighbor 10.100.0.4 description spine1-dc1_Ethernet2
   neighbor 10.100.0.6 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.100.0.6 remote-as 65100
   neighbor 10.100.0.6 description spine2-dc1_Ethernet2
   neighbor 10.100.0.131 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.100.0.131 remote-as 65000
   neighbor 10.100.0.131 description wan1-dc1_Ethernet2
   neighbor 10.100.0.135 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.100.0.135 remote-as 65000
   neighbor 10.100.0.135 description wan2-dc1_Ethernet2
   neighbor 10.100.1.1 peer group EVPN-OVERLAY-PEERS
   neighbor 10.100.1.1 remote-as 65100
   neighbor 10.100.1.1 description spine1-dc1
   neighbor 10.100.1.2 peer group EVPN-OVERLAY-PEERS
   neighbor 10.100.1.2 remote-as 65100
   neighbor 10.100.1.2 description spine2-dc1
   neighbor 10.100.4.0 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 10.100.4.0 description border1-dc1
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan 10
      rd 10.100.1.4:10010
      route-target both 10010:10010
      redistribute learned
   !
   vlan 20
      rd 10.100.1.4:10020
      route-target both 10020:10020
      redistribute learned
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf data
      rd 10.100.1.4:20
      route-target import evpn 20:20
      route-target export evpn 20:20
      router-id 10.100.1.4
      neighbor 10.100.0.131 remote-as 65000
      neighbor 10.100.0.131 peer group IPv4-UNDERLAY-PEERS
      neighbor 10.100.0.131 description wan1-dc1_Ethernet2.20_vrf_data
      neighbor 10.100.0.135 remote-as 65000
      neighbor 10.100.0.135 peer group IPv4-UNDERLAY-PEERS
      neighbor 10.100.0.135 description wan2-dc1_Ethernet2.20_vrf_data
      neighbor 10.100.4.0 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
   !
   vrf guest
      rd 10.100.1.4:10
      route-target import evpn 10:10
      route-target export evpn 10:10
      router-id 10.100.1.4
      neighbor 10.100.0.131 remote-as 65000
      neighbor 10.100.0.131 peer group IPv4-UNDERLAY-PEERS
      neighbor 10.100.0.131 description wan1-dc1_Ethernet2.10_vrf_guest
      neighbor 10.100.0.135 remote-as 65000
      neighbor 10.100.0.135 peer group IPv4-UNDERLAY-PEERS
      neighbor 10.100.0.135 description wan2-dc1_Ethernet2.10_vrf_guest
      neighbor 10.100.4.0 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 1200 | 1200 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 1200 min-rx 1200 multiplier 3
```

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
```

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.100.1.0/25 eq 32 |
| 20 | permit 10.100.2.0/25 eq 32 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 10.100.1.0/25 eq 32
   seq 20 permit 10.100.2.0/25 eq 32
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

##### RM-MLAG-PEER-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | origin incomplete | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
!
route-map RM-MLAG-PEER-IN permit 10
   description Make routes learned over MLAG Peer-link less preferred on spines to ensure optimal routing
   set origin incomplete
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| data | enabled |
| guest | enabled |
| MGMT | disabled |

### VRF Instances Device Configuration

```eos
!
vrf instance data
!
vrf instance guest
!
vrf instance MGMT
```

## EOS CLI Device Configuration

```eos
!
platform tfa personality arfa
```
