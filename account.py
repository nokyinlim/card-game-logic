import sqlite3
import json

from typing import Dict, Any


def update_account_stat(account_name: str, stat: str, value: float, operation: str = "add") -> Dict[str, str]:
    """
    Updates a given account stat with the given value, using the specified operation.
    :param account_name: The name of the account to update the stat for.
    :param stat: The name of the stat to update.
    :param value: The value to update the stat by.
    :param operation: The operation to perform on the stat. Can be 'add', 'subtract', 'multiply', or 'divide', or 'set'.
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
        case "subtract":
            stats[stat] -= value
        case "multiply":
            stats[stat] *= value
        case "divide":
            stats[stat] /= value
        case "set":
            stats[stat] = value
        case _:
            raise ValueError("Invalid operation. Please use 'add', 'subtract', 'multiply', or 'divide'.")

    # Convert the stats back to a string
    stats = json.dumps(stats)

    # Update the user's stats
    cursor.execute("UPDATE accounts SET stats=? WHERE username=?", (stats, account_name))

    # Save (commit) the changes
    conn.commit()

    # Close the connection
    conn.close()

    return {"message": "Stat updated successfully", "stats": stats}