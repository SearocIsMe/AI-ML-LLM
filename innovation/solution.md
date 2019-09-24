This section will talk about how to use Cloud-Native Concept/Architecture to make dream come true.

Before we start, several priciples need to be finalized so as to target the objectives in mind (You can sniff out what we will be doing, right?)
1. Cloud Service Provider Indepenpent.
2. User's Experience is must and first

- [Solution](#Solution)
  - [1. Stateless Sinkable Stream Processing](#1-Stateless-Sinkable-Stream-Processing)
    - [Resilent and Scaling](#Resilent-and-Scaling)
    - [Non-blocking Pipeline Pool](#Non-blocking-Pipeline-Pool)
    - [Elastic Pipeline](#Elastic-Pipeline)
  - [2. Foundamental Components](#2-Foundamental-Components)
  - [3. Architecture and Design Views](#3-Architecture-and-Design-Views)
  - [4. Put All Above Togehter](#4-Put-All-Above-Togehter)
  - [5. Software Engineering](#5-Software-Engineering)
    - [Development](#Development)
    - [Deployment](#Deployment-1)
    - [Monitoring/Operation](#MonitoringOperation)
    


# Solution

## 1. Stateless Sinkable Stream Processing

When I wrote this initiatives, I actally didnot notice friend from LightBend bas same understanding to Akka library, which is side topic for the thinking of how to solve current problem to fulfill the Cloud-Native principles.

### Resilent and Scaling

[TBD]

### Non-blocking Pipeline Pool

[TBD]

### Elastic Pipeline

[TBD]

## 2. Foundamental Components

"Pipeline As Service", aims to offer Cloud-Native service being built on top of real time, reactive streaming libraries, sitting in between the datasource and mutual Machine Learning Computing Cluster.

1. ["RSocket"](https://github.com/rsocket/rsocket) under ["Reactive Stream"](http://www.reactive-streams.org/) specification
2. For Java lang, ["Spring Boot RSocket"](https://github.com/CollaborationInEncapsulation/spring-boot-rsocket) is prefered.
3. It's recommanded to take a look ecosystem of Reactive Stream
   - ["akka"](https://akka.io/), Apache Flink uses this akka for resource management, mostly is from ["Alpakka"](https://doc.akka.io/docs/alpakka/current/)
   - [netifi](https://www.netifi.com/), github source
   - [Spring Reactive webflux](https://github.com/jdesigndev/spring-reactive-webflux)

## 3. Architecture and Design Views

[TBD]

## 4. Put All Above Togehter

Are you going to write another psudo "Spark" and "Flink" library?
[Answer] yes, 70% correct.

## 5. Software Engineering

### Development

What can stitch above ideas and existing, fantastic tools/library together? It's API exported by microservices.
[Swagger API Editor](http://editor.swagger.io/) is the powerful tool helping in API definition and generator the startup programming project.

### Deployment

Building a Prediction Service Without Running Spark/flink.

### Monitoring/Operation

Cluster Managament tools, "Manage Engine", "Nagios" are kind feature riched of daily operation and monitoring tools.
[TBD]