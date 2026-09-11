from app.database.database import get_connection


def create_item(name, description, status):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO items (name, description, status)
        VALUES (?, ?, ?)
        """,
        (name, description, status),
    )

    connection.commit()
    item_id = cursor.lastrowid
    connection.close()

    return item_id


def get_items():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, name, description, status FROM items"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_item(item_id):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, name, description, status FROM items WHERE id = ?",
        (item_id,),
    ).fetchone()

    connection.close()

    return dict(row) if row else None


def update_item(item_id, name, description, status):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE items
        SET name = ?, description = ?, status = ?
        WHERE id = ?
        """,
        (name, description, status, item_id),
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return None

    row = connection.execute(
        "SELECT id, name, description, status FROM items WHERE id = ?",
        (item_id,),
    ).fetchone()

    connection.close()

    return dict(row)


def delete_item(item_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM items WHERE id = ?",
        (item_id,),
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted
