
---

# 🌐 Computer Networks — Security & Cryptography Projects

> A structured academic repository containing **core Computer Networks security projects**, implemented from scratch with emphasis on **cryptography, trust establishment, secure communication, and protocol-level understanding**.

---

## 📌 Repository Overview

This repository contains **multiple concept-based projects** from the **Computer Networks / Network Security** curriculum.
Each project is organized into a **self-contained folder** with:

* 📄 A **detailed PDF report** (theory, design, message formats)
* 💻 A **Code** directory with complete implementations
* 🧠 Emphasis on **manual implementation**, not library shortcuts

The repository is designed to be:

* ✅ Easy to navigate
* ✅ Easy to evaluate
* ✅ Academically rigorous
* ✅ Portfolio-ready

---

## 🗂 Repository Structure (Visual Overview)

```
Computer-Networks
│
├── RSA_Based_Public_Key_Distribution_Authority
│   ├── RSA_Based_Public_Key_Distribution_Authority.pdf
│   └── Code
│       ├── pkda.py
│       ├── client1.py
│       ├── client2.py
│       └── README.md
│
├── Secure_Time_Stamping_of_Documents
│   ├── Secure_Time_Stamping_of_Documents.pdf
│   └── Code
│       ├── timestamp_server.py
│       ├── client.py
│       └── README.md
│
└── (more projects added as coursework progresses)
```

---

## 🔐 Project 1: RSA-Based Public Key Distribution Authority (PKDA)

### 🎯 Objective

To design and implement a **trusted Public Key Distribution Authority (PKDA)** using **RSA cryptography**, enabling clients to:

* Securely obtain **their own public keys**
* Securely request **other clients’ public keys**
* Establish **confidential peer-to-peer communication**

---

### 🧩 System Architecture (Visual)

```
        ┌──────────────┐
        │     PKDA     │
        │ (Trusted CA) │
        └──────┬───────┘
               │  RSA-signed
               │  public keys
   ┌───────────┴───────────┐
   │                       │
┌──▼───┐               ┌───▼───┐
│Client│               │Client │
│  A   │◀──Encrypted──▶│   B   │
└──────┘               └───────┘
```

---

### 🔄 Secure Message Flow

**Public Key Request**

```
Client A → PKDA :
{ ID_A, ID_B, Timestamp, Nonce }

PKDA → Client A :
{ PK_B, ID_B, Validity, Timestamp, Signature_PKDA }
```

**Secure Communication**

```
Client A → Client B :
Encrypt( Message, PK_B )
```

---

### 🛡 Security Features

✔ RSA public-key cryptography
✔ PKDA acts as a **trusted authority**
✔ Nonces prevent replay attacks
✔ Timestamps ensure freshness
✔ Clients never trust unauthenticated keys

---

### 📁 Folder Contents

* **PDF**

  * Problem statement
  * Protocol design
  * Message formats
  * Security analysis
  * Sample execution logs
* **Code**

  * `pkda.py` → PKDA server
  * `client1.py`, `client2.py` → communicating clients

---

## ⏱ Project 2: Secure Time-Stamping of Documents

### 🎯 Objective

To ensure **proof of document existence at a specific time** using cryptographic techniques, preventing:

* Back-dating
* Tampering
* Forgery

---

### 🧠 Core Idea

Instead of trusting a document’s local timestamp, the system uses a **trusted Time-Stamping Authority (TSA)**.

---

### 🔄 Time-Stamping Workflow (Visual)

```
Client
  │
  │ Hash(Document)
  │
  ▼
┌──────────────┐
│  Time Server │
│   (TSA)      │
└──────┬───────┘
       │
       │ { Hash, Time, Signature_TSA }
       ▼
Client stores cryptographic proof
```

---

### 🔐 Cryptographic Guarantees

✔ Document integrity
✔ Non-repudiation
✔ Trusted timestamp
✔ Tamper evidence

---

### 📁 Folder Contents

* **PDF**

  * Time-stamping protocol
  * Threat model
  * Cryptographic justification
  * Use-cases
* **Code**

  * `timestamp_server.py` → TSA server
  * `client.py` → document submitter & verifier

---

## 🧠 Design Philosophy of This Repository

### Why concept-based folders?

❌ Assignment_1
❌ Week_3

✅ RSA_Based_Public_Key_Distribution_Authority
✅ Secure_Time_Stamping_of_Documents

➡ Shows **what you built**, not just *when* you built it.

---

### Why PDF + Code separation?

* PDFs explain **what & why**
* Code shows **how**
* Evaluators can assess both independently

---

## 🎓 Academic Alignment

This repository demonstrates mastery of:

* Public-key cryptography
* Trust establishment
* Secure protocol design
* Replay protection
* Real-world security assumptions
* Manual implementation (no black-box libraries)

---

## 🚀 How to Use This Repository

1. Open a project folder
2. Read the **PDF** for protocol & design
3. Open **Code/** for implementation
4. Run programs as explained in the project README

---

## 📌 Future Extensions

* DES / AES manual implementation
* Secure socket programming
* Firewall & IDS simulations
* TLS handshake modeling

---

## ✅ Final Note

This repository is intended to be:

* **Instructor-friendly**
* **Technically correct**
* **Security-focused**
* **Portfolio-ready**

---


Just say 👍
