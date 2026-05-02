# OSPF Multi-Area NetDevOps Lab

## Project Overview

This lab demonstrates a multi-area OSPF topology built in Cisco Modeling Labs and managed using beginner NetDevOps practices.

The goal of this project is to reinforce OSPF design fundamentals while learning how network engineers can use automation, validation, version control, and CI/CD workflows to manage network changes.

## Lab Goals

- Build a multi-area OSPF topology in Cisco Modeling Labs
- Use Area 0 as the OSPF backbone
- Connect all non-backbone areas back to Area 0
- Validate OSPF neighbor relationships before changes
- Use automation to push a controlled network change
- Validate OSPF routing after the change
- Track all code and configuration changes with Git and GitHub

## Topology Design

The lab uses five routers:

| Router | Role | OSPF Area |
|---|---|---|
| R1 | Backbone Router / ABR | Area 0, Area 10 |
| R2 | Backbone Router / ABR | Area 0, Area 20, Area 30 |
| R3 | Internal Router | Area 10 |
| R4 | Internal Router | Area 20 |
| R5 | Internal Router | Area 30 |

## OSPF Area Layout

| Link | OSPF Area |
|---|---|
| R1 to R2 | Area 0 |
| R1 to R3 | Area 10 |
| R2 to R4 | Area 20 |
| R2 to R5 | Area 30 |

## NetDevOps Workflow

This project will follow a simple network automation workflow:

1. Build the baseline topology
2. Configure OSPF manually first
3. Validate the baseline network state using pyATS
4. Use Ansible to push a controlled change
5. Run post-change validation using pyATS
6. Commit the changes to GitHub
7. Use GitLab CI/CD for linting and pipeline checks

## Planned Automation Change

The first automated change will add a loopback interface to R3 and advertise it into OSPF Area 10.

Expected result:

- R3 has a new Loopback30 interface
- The loopback route appears in the OSPF routing tables of the other routers
- OSPF neighbor relationships remain stable

## Skills Practiced

- OSPF multi-area design
- Cisco IOS configuration
- Cisco Modeling Labs
- Git and GitHub
- Cisco pyATS network validation
- Ansible automation
- GitLab CI/CD fundamentals

## Current Status

- Topology built in Cisco Modeling Labs
- IP addressing configured across all routers
- Multi-area OSPF configured successfully
- All OSPF neighbors are in FULL state
- Inter-area routing verified across backbone

## Validation Commands Used

- show ip ospf neighbor
- show ip route ospf
- show ip ospf interface brief

## Completed Workflow

This lab now demonstrates a basic NetDevOps workflow:

1. Built a multi-area OSPF topology in Cisco Modeling Labs
2. Established SSH access to all IOSv routers
3. Created a pyATS testbed file for device connectivity
4. Wrote a Python validation script to check OSPF neighbor state
5. Added route validation for OSPF-learned networks
6. Used Ansible to add Loopback30 to R3
7. Advertised 10.30.30.30/32 into OSPF Area 10
8. Re-ran validation to confirm the loopback route propagated to R1, R2, R4, and R5

## Validation Results

The pyATS validation script confirms:

- All expected OSPF neighbors are in FULL state
- OSPF routes are present in the routing table
- The new loopback route `10.30.30.30/32` is learned by remote routers after the Ansible change