from confluent_kafka import TopicPartition as GroupPartitionMetadata
from confluent_kafka.admin import BrokerMetadata
from confluent_kafka.admin import GroupMember as GroupMemberMetadata
from confluent_kafka.admin import GroupMetadata, PartitionMetadata, TopicMetadata

from kaskade.kafka.models import (
    Broker,
    Group,
    GroupMember,
    GroupPartition,
    Partition,
    Topic,
)


def metadata_to_broker(metadata: BrokerMetadata) -> Broker:
    return Broker(id=metadata.id, host=metadata.host, port=metadata.port)


def metadata_to_group(metadata: GroupMetadata) -> Group:
    return Group(
        id=metadata.id,
        broker=metadata_to_broker(metadata.broker),
        state=metadata.state,
        members=[],
        partitions=[],
    )


def metadata_to_group_member(metadata: GroupMemberMetadata) -> GroupMember:
    return GroupMember(
        id=metadata.id,
        group="",
        client_id=metadata.client_id,
        client_host=metadata.client_host,
    )


def metadata_to_group_partition(metadata: GroupPartitionMetadata) -> GroupPartition:
    return GroupPartition(
        id=metadata.partition,
        topic=metadata.topic,
        offset=metadata.offset,
        group="",
        high=0,
        low=0,
    )


def metadata_to_partition(metadata: PartitionMetadata) -> Partition:
    return Partition(
        id=metadata.id,
        leader=metadata.leader,
        replicas=metadata.replicas,
        isrs=metadata.isrs,
        high=0,
        low=0,
    )


def metadata_to_topic(metadata: TopicMetadata) -> Topic:
    name = metadata.topic
    return Topic(
        name=name,
        groups=[],
        partitions=[],
    )
