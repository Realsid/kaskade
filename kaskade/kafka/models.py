import datetime
from typing import Any, List, Optional, Tuple


class Broker:
    def __init__(self, id: int = -1, host: str = "", port: int = -1) -> None:
        self.id = id
        self.host = host
        self.port = port

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "{}:{}/{}".format(self.host, self.port, self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Broker):
            return self.id == other.id
        return False


class GroupMember:
    def __init__(
        self,
        id: str = "",
        client_id: str = "",
        group: str = "",
        client_host: str = "",
    ) -> None:
        self.id = id
        self.client_id = client_id
        self.group = group
        self.client_host = client_host

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(
            {
                "id": self.id,
                "group": self.group,
                "client_id": self.client_id,
                "client_host": self.client_host,
            }
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, GroupMember):
            return self.id == other.id
        return False


class GroupPartition:
    def __init__(
        self,
        id: int = -1,
        topic: str = "",
        group: str = "",
        offset: int = 0,
        low: int = 0,
        high: int = 0,
    ) -> None:
        self.id = id
        self.topic = topic
        self.group = group
        self.offset = offset
        self.low = low
        self.high = high

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(
            {
                "id": self.id,
                "group": self.group,
                "topic": self.topic,
                "offset": self.offset,
                "low": self.low,
                "high": self.high,
            }
        )

    def lag_count(self) -> int:
        if self.high < 0:
            return 0
        elif self.offset < 0:
            return self.high - self.low
        else:
            return self.high - self.offset

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, GroupPartition):
            return self.id == other.id
        return False


class Group:
    def __init__(
        self,
        id: str = "",
        broker: Broker = Broker(),
        state: str = "",
        members: List[GroupMember] = [],
        partitions: List[GroupPartition] = [],
    ) -> None:
        self.broker = broker
        self.id = id
        self.state = state
        self.members = members
        self.partitions = partitions

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.id

    def lag_count(self) -> int:
        return (
            sum([partition.lag_count() for partition in self.partitions])
            if self.partitions is not None
            else 0
        )

    def members_count(self) -> int:
        return len(self.members) if self.members is not None else 0

    def partitions_count(self) -> int:
        return len(self.partitions) if self.partitions is not None else 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Group):
            return self.id == other.id
        return False


class Partition:
    def __init__(
        self,
        id: int = -1,
        leader: int = -1,
        replicas: List[int] = [],
        isrs: List[int] = [],
        low: int = 0,
        high: int = 0,
    ) -> None:
        self.id = id
        self.leader = leader
        self.replicas = replicas
        self.isrs = isrs
        self.low = low
        self.high = high

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.id)

    def messages_count(self) -> int:
        return self.high - self.low

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Partition):
            return self.id == other.id
        return False


class Topic:
    def __init__(
        self,
        name: str = "",
        partitions: List[Partition] = [],
        groups: List[Group] = [],
    ) -> None:
        self.name = name
        self.partitions = partitions
        self.groups = groups

    def partitions_count(self) -> int:
        return len(self.partitions) if self.partitions is not None else 0

    def groups_count(self) -> int:
        return len(self.groups) if self.groups is not None else 0

    def replicas_count(self) -> int:
        return (
            max([len(partition.replicas) for partition in self.partitions], default=0)
            if self.partitions is not None
            else 0
        )

    def isrs_count(self) -> int:
        return (
            min([len(partition.isrs) for partition in self.partitions], default=0)
            if self.partitions is not None
            else 0
        )

    def lag_count(self) -> int:
        return (
            max([group.lag_count() for group in self.groups], default=0)
            if self.groups is not None
            else 0
        )

    def messages_count(self) -> int:
        return (
            sum([partition.messages_count() for partition in self.partitions])
            if self.partitions is not None
            else 0
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Topic):
            return self.name == other.name
        return False


class Cluster:
    def __init__(
        self,
        brokers: List[Broker] = [],
        version: str = "",
        has_schemas: bool = False,
        protocol: str = "plain",
    ) -> None:
        self.brokers = brokers
        self.version = version
        self.has_schemas = has_schemas
        self.protocol = protocol

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(
            {
                "brokers": self.brokers,
                "version": self.version,
                "has_schemas": self.has_schemas,
                "protocol": self.protocol,
            }
        )

    def brokers_count(self) -> int:
        return len(self.brokers) if self.brokers is not None else 0


class Record:
    def __init__(
        self,
        date: Optional[datetime.datetime] = None,
        partition: int = -1,
        offset: int = -1,
        headers: Optional[List[Tuple[str, bytes]]] = None,
        key: Optional[bytes] = None,
        value: Optional[bytes] = None,
    ) -> None:
        self.date = date
        self.partition = partition
        self.offset = offset
        self.headers = headers
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(
            {
                "date": str(self.date),
                "partition": self.partition,
                "offset": self.offset,
                "header": self.headers,
                "key": self.key,
                "value": self.value,
            }
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Record):
            return self.partition == other.partition and self.offset == other.offset
        return False
