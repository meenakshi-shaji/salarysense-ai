import sqlite3

# =========================================
# CONNECT DATABASE
# =========================================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

c = conn.cursor()

# =========================================
# USERS TABLE
# =========================================

c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (

        username TEXT,
        password TEXT
    )
    """
)

# =========================================
# PREDICTIONS TABLE
# =========================================

c.execute(
    """
    CREATE TABLE IF NOT EXISTS predictions (

        username TEXT,
        job_role TEXT,
        location TEXT,
        experience INTEGER,
        salary TEXT
    )
    """
)

conn.commit()

# =========================================
# ADD USER
# =========================================

def add_user(
    username,
    password
):

    c.execute(
        """
        INSERT INTO users
        VALUES (?, ?)
        """,
        (
            username,
            password
        )
    )

    conn.commit()

# =========================================
# LOGIN USER
# =========================================

def login_user(
    username,
    password
):

    c.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            password
        )
    )

    return c.fetchone()

# =========================================
# UPDATE USERNAME
# =========================================

def update_username(
    old_username,
    new_username
):

    c.execute(
        """
        UPDATE users
        SET username=?
        WHERE username=?
        """,
        (
            new_username,
            old_username
        )
    )

    conn.commit()

# =========================================
# UPDATE PASSWORD
# =========================================

def update_password(
    username,
    new_password
):

    c.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            new_password,
            username
        )
    )

    conn.commit()

# =========================================
# SAVE PREDICTION
# =========================================

def save_prediction(
    username,
    job_role,
    location,
    experience,
    salary
):

    c.execute(
        """
        INSERT INTO predictions
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            job_role,
            location,
            experience,
            salary
        )
    )

    conn.commit()

# =========================================
# GET PREDICTIONS
# =========================================

def get_predictions(
    username
):

    c.execute(
        """
        SELECT
        job_role,
        location,
        experience,
        salary

        FROM predictions

        WHERE username=?
        """,
        (
            username,
        )
    )

    return c.fetchall()