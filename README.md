# LIFT

**Linux Investigation & Forensics Toolkit**

LIFT is a personal learning project focused on Linux telemetry collection, event reconstruction, session awareness, and detection engineering.

The goal of the project is to understand how modern security products process operating system telemetry and transform raw audit events into meaningful security investigations.

---

## Current Objectives

* Learn Linux internals
* Learn auditd telemetry
* Understand event correlation
* Build session awareness
* Develop detection engineering skills
* Explore threat hunting workflows

---

## Current Architecture

```text
auditd
   ↓
AuditRecord
```

### Planned Architecture

```text
auditd
   ↓
AuditRecord
   ↓
LogicalEvent
   ↓
Session
   ↓
Detection Playbooks
```

---

## Current Features

### Audit Parsing

The parser currently extracts:

* Record Type
* Audit Serial Number
* Timestamp
* Dynamic key=value fields

Example:

```json
{
    "record_type": "SYSCALL",
    "serial": "91328",
    "timestamp": "06/15/2026 09:23:45.328",
    "fields": {
        "pid": "1217",
        "uid": "kali",
        "exe": "/usr/bin/xfdesktop"
    }
}
```

---

## Project Status

### Completed

* Generic AuditRecord abstraction
* Audit serial extraction
* Timestamp extraction
* Dynamic field extraction
* Audit sample generation

### In Progress

* Event assembly
* Logical event reconstruction
* Session tracking redesign

### Planned

* Playbook engine
* Detection rules
* Timeline correlation
* eBPF telemetry integration

---

## Learning Goals

This project is intentionally being built from scratch to understand:

* Linux auditing
* Process execution telemetry
* User identity tracking
* Privilege transitions
* Security event correlation
* Detection engineering concepts

---

## Disclaimer

LIFT is an educational project and is currently under active development.
