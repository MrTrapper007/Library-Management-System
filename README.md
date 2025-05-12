# Library-Management-System
Algorithms and Data Structures Final Project


Authors: Lucca Arantes, Riad Al Zaim, Moaz Ashry

Course: Algorithms and Data Structures

Supervisor: Shamli Shamli

Department: Computer Science

University: SRH Campus Leipzig

Date of Submission: 2025/05/12

# Abstract

This project presents a Python-based Library Management System aimed at providing a simple, intuitive GUI for librarians to manage core operations such as book borrowing, user management, and cataloging. Motivated by the need for an accessible and efficient tool in library environments, our team developed a modular system using object-oriented principles. The backend logic handles books, users, and borrowing mechanics, while the GUI offers a user-friendly interface. Key features include book and user management, searching by various criteria, waiting lists, and persistent data saving. The primary result is a fully functional desktop application with clear code separation and maintainability. This system sets the groundwork for future features like multi-client access and macOS support.

# Table of Contents:

1. Introduction

2. Background / Related Work

3. Methodology / System Design

4. Implementation

5. Evaluation / Results

6. Discussion

7. Conclusion and Future Work

# Appendices

- ### **Chapter 1: Introduction**

**1.1 Background and Motivation**

Managing a library's operations manually can be inefficient and error-prone. This project addresses this by creating a lightweight, GUI-based system that enables librarians to manage key tasks effectively, even without extensive technical knowledge.

**1.2 Problem Statement**

Libraries often lack affordable and easy-to-use software solutions for managing their operations. Our system aims to fill this gap by delivering a basic but effective library management tool.

**1.3 Objectives**

Develop a user-friendly library management application with a GUI.

Implement functions to add/delete books and users.

Enable borrowing, returning, and tracking of books.

Incorporate search and filter features.

Support saving and loading of data.

**1.4 Scope and Limitations**

Scope: Desktop-based library management.Limitations: No network-based multi-client functionality, limited macOS support.

**1.5 Contribution**

A structured Python application that separates logic, GUI, and data objects to ensure maintainability and usability.

**1.6 Report Structure**

Chapter 2 reviews related systems. Chapter 3 discusses our design and methods. Chapter 4 presents the implementation. Chapter 5 details the evaluation. Chapter 6 provides discussion, and Chapter 7 concludes with future work.

- ### **Chapter 2: Background / Related Work**

Several commercial and open-source library systems exist (e.g., Koha, Evergreen), but many are overly complex or server-based. Our approach is lightweight, suitable for small-scale libraries. We referenced design patterns like MVC and basic object-oriented practices to ensure code clarity and maintainability. Gaps addressed include simplicity, local operation, and an intuitive interface.

- ### **Chapter 3: Methodology / System Design**

**3.1 Overall Architecture**

The system is divided into:

Logic Module: Handles book/user operations.

Object Classes: Defines Book, User, etc.

GUI Module: User interface logic.

**3.2 Algorithms and Data Structures**

Waiting List: Queue-based structure.

Search: Basic filtering using list comprehension and attribute matching.

**3.3 Design Choices**

We opted for Python due to its readability and GUI libraries. The team used file separation to support modularity and collaboration.

- ### **Chapter 4: Implementation**

**4.1 Tools and Technologies**

Language: Python

IDE: JetBrains PyCharm

Version Control: Git/GitHub

**4.2 Key Implementation Details**

Book/User classes contain basic attributes and methods.

Borrow logic includes date tracking and user queues.

GUI integrates backend functions into user actions.

**4.3 Development Process**

GitHub was used for version control. The team divided responsibilities logically: Lucca (backend/logic), Riad and Moaz (GUI and integration).

- ### Chapter 5: Evaluation / Results
**5.1 Evaluation Strategy**

Manual testing for all operations and GUI interaction. Simulated multiple borrow/return cases.

**5.2 Results**

Book search and management worked reliably.

Data saving/loading tested across sessions.

Waiting list logic handled concurrency correctly.


- ### **Chapter 6: Discussion**

**6.1 Objective Assessment**

Most functional goals were met. GUI is stable, and logic integrates seamlessly.

**6.2 Limitations**

No real-time multi-user syncing.

Compatibility issues on macOS.

**6.3 Comparisons**

While less feature-rich than enterprise systems, our system excels in simplicity and clarity.

- ### **Chapter 7: Conclusion and Future Work**

**7.1 Summary**

We built a Python-based desktop library system that meets core management needs with a user-friendly GUI and clean codebase.

**7.2 Future Work**

Multi-client real-time syncing.

Improve macOS support.

Enhanced user access control.

**Appendices**

A. GitHub Repository Link

B. GUI Screenshots

C. Class Diagrams

