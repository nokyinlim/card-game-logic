import sqlite3
import json

from typing import Dict, Any


def get_account_stat(account_name: str, stat: str):
    """
    Gets a specific stat for a given account.
    """
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    # Select the current user's stats
    stats = cursor.execute("SELECT stats FROM accounts WHERE username=?", (account_name,))
    stats = stats.fetchone()[0]

    # Convert the stats from a string to a dictionary
    stats = json.loads(stats)

    conn.close()

    return stats[stat]


def get_account_stats(account_name: str) -> Dict[str, float]:
    """
    Gets all stats for a given account.
    """

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    # Select the current user's stats
    stats = cursor.execute("SELECT stats FROM accounts WHERE username=?", (account_name,))
    stats = stats.fetchone()[0]

    # Convert the stats from a string to a dictionary
    stats = json.loads(stats)

    conn.close()

    return stats

def update_account_stat(account_name: str, stat: str, value: float = 1, operation: str = "add") -> Dict[str, str]:
    """
    Updates a given account stat with the given value, using the specified operation.
    :param account_name: The name of the account to update the stat for.
    :param stat: The name of the stat to update.
    :param value: The value to update the stat by.
    :param operation: The operation to perform on the stat. Can be 'add', 'subtract', 'multiply', or 'divide', or 'set'.
    If no values are given, it defaults to adding by 1.
    :return: A dictionary containing a message and the stringified updated stats. Keys: 'message', 'stats'.
    """
    # Connect to an SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('database.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Select the current user's stats
    stats = cursor.execute("SELECT stats FROM accounts WHERE username=?", (account_name,))
    stats = stats.fetchone()[0]

    # Convert the stats from a string to a dictionary
    stats = json.loads(stats)

    # Update the specific stat
    match operation:
        case "add":
            stats[stat] += value
        case "subtract": # also why this...
            stats[stat] -= value
        case "multiply":
            stats[stat] *= value
        case "divide": # why would you ever need this lol
            stats[stat] /= value
        case "set":
            stats[stat] = value
        case _:
            raise ValueError("Invalid operation. Please use 'add', 'subtract', 'multiply', or 'divide'.")


    stats = json.dumps(stats)
    
    cursor.execute("UPDATE accounts SET stats=? WHERE username=?", (stats, account_name))
    conn.commit()
    conn.close()

    return {"message": "Stat updated successfully", "stats": stats}