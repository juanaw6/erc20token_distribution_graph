# ERC-20 Token Distribution Graph

![GitHub last commit](https://img.shields.io/github/last-commit/juanaw6/erc20token_distribution_graph)
![GitHub license](https://img.shields.io/github/license/juanaw6/erc20token_distribution_graph)

This repository contains a Python script that generates a distribution graph for ERC-20 tokens on the Ethereum blockchain. The script uses the Covalent API to collect data about token holders and their transactions, creates a weighted graph representing these transactions, and applies the Louvain clustering algorithm to identify communities within the token holder network.

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)

## Overview

The ERC-20 Token Distribution Graph script is designed to provide insights into the distribution of ERC-20 tokens within the Ethereum ecosystem. It focuses on analyzing how token holders interact with each other through transactions and identifies communities or clusters of token holders with strong transactional connections.

The key features of this repository include:

- Data collection using the Covalent API to gather information about token holders and their transactions.
- Construction of a weighted graph that represents the relationships between token holders.
- Application of the Louvain clustering algorithm to partition token holders into communities based on their transactional interactions.
- Visualization of the resulting communities within the token holder network.

## Usage

To use this script, follow these steps:
1. Make sure you have Python installed on your system. You can download and install Python from the [official python website](https://www.python.org/downloads/).
2. Make sure you have created a Covalent and an Etherscan API key. You can setup one from [Covalent](https://www.covalenthq.com/docs/api/) and [Etherscan](https://etherscan.io/) official website.
3. Clone the repository to your local machine:

   ```
   git clone https://github.com/juanaw6/erc20token_distribution_graph.git
   ```
4. Navigate to the project directory:
   ```
   cd erc20token_distribution_graph
   ```
5. Install the required Python packages using pip:
   ```
   pip install -r requirements.txt
   ```
6. Replace the placeholder values in the config.py file with your Covalent and Etherscan API key and the Ethereum contract address of the ERC-20 token you want to analyze.
7. Run the main Python script, the script will collect data and store it in contract_addr.json and holder.json:
   ```
   python main.py
   ```
8. To construct the graph, apply the Louvain clustering algorithm, and generate visualizations of the token holder communities:
   ```
   python draw_graph.py
   ```
   or to just construct the graph without connection from or to token node for better community visualization:
   ```
   python draw_community.py
   ```
