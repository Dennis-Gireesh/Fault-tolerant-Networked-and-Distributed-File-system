# Fault-tolerant-Networked-and-Distributed-File-system
Principles of Computer System Design

## Introduction and problem statement:
	This project implements the practical multi server’s/client files system (the file servers running on the same computer) with networking and fault tolerance with support of Redundant Array of Independent Disks (RAID5) block storage approach. RAID 5 is a data backup technology for hard disk drives that uses both disk striping and parity. It is one of the levels of RAID: Redundant Array of Independent Disks, originally Inexpensive Disks. In practice, RAID5 usually offers a good balance between security, fault tolerance, and performance, hence highly efficient for data storage. These servers just aware about the raw block layer of the filesystem. The rest of the filesystem layers and caching are implemented in the Memory_client.py. Server just exposes Get() and Put() interfaces. This project aims to distribute and store the data across the multiple data servers in order to reduce the load on each server (servers holding the copies of data), to provide large aggregated storage capacity with the fault tolerance mechanism while operation of the system. The system is robustly designed which handles the failure scenarios like Fail-stop of a server with repair mechanism and force corruption of a block in any server to emulates the failure. This system performance is analyzed by calculating the average load on the multiple servers (number of requests handled per server) against the single server system.
## Design and implementation:
  - Support of multiple servers
  - Virtual to Physical address conversion(RAID5 Mapping)
  - Adding Checksum
  - Send/Recive data API's
  - Corruption of data
  - Fail-stop of the server
  - Repair
  - Evaluation
  - Performance
  
The average load on each server = (Total No.of Requests)/(Total no.of servers)

| Server |	No. of requests|
|--------| ---------|
|Server 0|	846|
|Server 1|	899|
|Server 2|	889|
|Server 3|	887|
|Server 4| 868|

## Conclusions
o	This project implemented multi-server single client-based file system where clients accessed data blocks stored at a server.
o	Design of systems including: client/service, networking, and fault tolerance with support of Redundant Array of Independent Disks (RAID5) block storage approach.
o	The Mapping function in the system can be adjusted to work the system like any other RAID versions (like RAID 4, RAID5…)
o	This files system is implemented using checksum which helps to identify any errors in the system and this design doesn’t include the RSM locks mechanism.
o	Designed is robust enough to handle and mitigate the failure scenarios like, Corrupt block (only one) and Fail-stop of server.
o	The repair mechanism is implemented to bring the server back with its old contents to which resumes normal operation.
o	This file system design cannot handle more than two failures in a system at any given time.
o	It is observed that, for multi-server system the load on each server is decreased by almost 30%, with a single server system (allowing few implementation changes between two servers).

