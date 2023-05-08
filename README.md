## The Problem
Obviously, there are tons of different ways to
synchronize distributed databases. Let's imagine that
we have an unusual situation with restrictions below:
- A future system will have some Head Office (HO)
and a couple of Branch Offices (BOs).
- All offices are located in different places, and some
of them have limitation with the internet
connection. It could even be a situation where the
internet is available for 1-2 hours per day.

The perfect solution is to write your own DB sync
mechanism data between branches using RabbitMQ
Message queues.

For this lab we assume one Head Office (HO) and 2
Branch offices (BO) for sales. The 2 sales branches are
physically separated from the Head office. They manage
their databases independently and they need to
synchronise their data to the Head office that maintain
the hole data of sales. We assume that the database are
based on the product sales table with the following
structure.

The main of this lab is to create a distributed application
that synchronisation databases from the product sales
tables. This application needs to use the RabbitMQ to
send data on the related queues. We run 2 distributed
processes that synchronise data from first BO to HO and
the second BO to the HO. 