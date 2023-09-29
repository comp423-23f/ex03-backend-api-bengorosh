"""Tests for the mock storage layer."""

from services.storage import StorageService
from models.user import User
import pytest


@pytest.fixture(autouse=True)
def storage_service():
    """This PyTest fixture is injected into each test parameter of the same name below.

    It constructs a new, empty StorageService object."""
    storage_service = StorageService()
    storage_service.reset()
    return storage_service


def test_get_registrations_empty(storage_service: StorageService):
    assert len(storage_service.get_registrations()) == 0


def test_create_registration_valid(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    users = storage_service.get_registrations()
    assert len(users) == 1
    assert users[0].pid == pid


def test_create_registration_invalid_pid(storage_service: StorageService):
    pid = 71045308
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_create_registration_missing_first_name(storage_service: StorageService):
    pid = 71045308
    user = User(pid=pid, first_name="", last_name="Jordan")
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_create_registration_missing_last_name(storage_service: StorageService):
    pid = 71045308
    user = User(pid=pid, first_name="Kris", last_name="")
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_create_registration_duplicate(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_get_user_by_pid_does_not_exist(storage_service: StorageService):
    assert storage_service.get_user_by_pid(710453084) is None


def test_get_user_by_pid_does_exist(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    assert storage_service.get_user_by_pid(710453084) is user


def test_create_checkin_unknown_pid(storage_service: StorageService):
    with pytest.raises(Exception):
        storage_service.create_checkin(710453084)


def test_create_checkin_produces_checkin(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    storage_service.create_checkin(pid)
    checkins = storage_service.get_checkins()
    assert len(checkins) == 1
    assert checkins[0].user == user


def test_delete_registration_not_right_length_pid(storage_service: StorageService):
    pid = 71045308
    user = User(pid=710453084, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    with pytest.raises(Exception):
        storage_service.delete_registration(pid)


def test_delete_registration_invalid_pid(storage_service: StorageService):
    pid = 730470759
    user = User(pid=710453084, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    with pytest.raises(Exception):
        storage_service.delete_registration(pid)


def test_delete_registration_valid_pid(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    users = storage_service.get_registrations()
    assert len(users) == 1
    assert users[0].pid == pid
    storage_service.delete_registration(pid)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 0


def test_delete_registration_checkins_registrations(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    storage_service.create_checkin(pid)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 1
    assert users[0].pid == pid
    assert len(checkins) == 1
    assert checkins[0].user.pid == pid
    storage_service.delete_registration(pid)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 0
    assert len(checkins) == 0


def test_delete_registration_delete_first(storage_service: StorageService):
    pid1 = 123456789
    pid2 = 730470759
    user1 = User(pid=pid1, first_name="Ben", last_name="Gor")
    user2 = User(pid=pid2, first_name="Alex", last_name="G")
    storage_service.create_registration(user1)
    storage_service.create_checkin(pid1)
    storage_service.create_registration(user2)
    storage_service.create_checkin(pid2)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 2
    assert users[0].pid == pid1
    assert len(checkins) == 2
    assert checkins[0].user.pid == pid1
    storage_service.delete_registration(pid1)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 1
    assert users[0].pid == pid2
    assert len(checkins) == 1
    assert checkins[0].user.pid == pid2


def test_delete_registration_delete_middle(storage_service: StorageService):
    pid1 = 123456789
    pid2 = 730470759
    pid3 = 987654321
    user1 = User(pid=pid1, first_name="Ben", last_name="Gor")
    user2 = User(pid=pid2, first_name="Alex", last_name="G")
    user3 = User(pid=pid3, first_name="Alex", last_name="G")
    storage_service.create_registration(user1)
    storage_service.create_checkin(pid1)
    storage_service.create_registration(user2)
    storage_service.create_checkin(pid2)
    storage_service.create_registration(user3)
    storage_service.create_checkin(pid3)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 3
    assert users[2].pid == pid3
    assert len(checkins) == 3
    assert checkins[2].user.pid == pid3
    storage_service.delete_registration(pid2)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 2
    assert users[1].pid == pid3
    assert users[0].pid == pid1
    assert len(checkins) == 2
    assert checkins[1].user.pid == pid3
    assert checkins[0].user.pid == pid1


def test_delete_registration_delete_last(storage_service: StorageService):
    pid1 = 123456789
    pid2 = 730470759
    user1 = User(pid=pid1, first_name="Ben", last_name="Gor")
    user2 = User(pid=pid2, first_name="Alex", last_name="G")
    storage_service.create_registration(user1)
    storage_service.create_checkin(pid1)
    storage_service.create_registration(user2)
    storage_service.create_checkin(pid2)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 2
    assert users[0].pid == pid1
    assert len(checkins) == 2
    assert checkins[0].user.pid == pid1
    storage_service.delete_registration(pid2)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 1
    assert users[0].pid == pid1
    assert len(checkins) == 1
    assert checkins[0].user.pid == pid1


def test_delete_registration_delete_same(storage_service: StorageService):
    pid1 = 123456789
    pid2 = 730470759
    user1 = User(pid=pid1, first_name="Ben", last_name="Gor")
    user2 = User(pid=pid2, first_name="Alex", last_name="G")
    storage_service.create_registration(user1)
    storage_service.create_checkin(pid1)
    storage_service.create_registration(user2)
    storage_service.create_checkin(pid2)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 2
    assert users[0].pid == pid1
    assert users[1].pid == pid2
    assert len(checkins) == 2
    assert checkins[0].user.pid == pid1
    assert checkins[1].user.pid == pid2
    storage_service.delete_registration(pid2)
    users = storage_service.get_registrations()
    checkins = storage_service.get_checkins()
    assert len(users) == 1
    assert users[0].pid == pid1
    assert len(checkins) == 1
    assert checkins[0].user.pid == pid1
    with pytest.raises(Exception):
        storage_service.delete_registration(pid2)