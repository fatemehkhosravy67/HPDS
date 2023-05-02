from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from datetime import datetime, timedelta
from database import Base, get_db, RAMUsage
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_ram_usage():
    # Add test data to the database
    with TestingSessionLocal() as db:
        db.add(RAMUsage(total=16.0, free=4.0, used=12.0, timestamp=datetime.utcnow()))
        db.add(RAMUsage(total=16.0, free=3.0, used=13.0, timestamp=datetime.utcnow() - timedelta(hours=1)))
        db.add(RAMUsage(total=16.0, free=2.0, used=14.0, timestamp=datetime.utcnow() - timedelta(hours=2)))
        db.add(RAMUsage(total=16.0, free=1.0, used=15.0, timestamp=datetime.utcnow() - timedelta(hours=3)))
        db.add(RAMUsage(total=16.0, free=0.0, used=16.0, timestamp=datetime.utcnow() - timedelta(hours=4)))
        db.commit()

        # Test reading 3 most recent rows
        response = client.get("/ram_usage/?n=3")
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["free"] == 4.0
        assert response.json()[1]["free"] == 3.0
        assert response.json()[2]["free"] == 2.0

        # Test reading 10 rows when there are less than 10 rows in the database
        response = client.get("/ram_usage/?n=10")
        assert response.status_code == 200

        # Test reading 0 rows
        response = client.get("/ram_usage/?n=0")
        assert response.status_code == 400

        # Test reading n rows when n equals to the number of rows in the database
        response = client.get("/ram_usage/?n=5")
        assert response.status_code == 200
        assert len(response.json()) == 5
        assert response.json()[0]["free"] == 4.0
        assert response.json()[1]["free"] == 3.0
        assert response.json()[2]["free"] == 2.0
        assert response.json()[3]["free"] == 1.0
        assert response.json()[4]["free"] == 0.0

        # Test reading n rows when n is greater than the number of rows in the database
        response = client.get("/ram_usage/?n=6")
        assert response.status_code == 200
