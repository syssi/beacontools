"""Beacon advertisement parser."""
import traceback

from construct import ConstructError

from .structs import EddystoneFrame
from .packet_types import EddystoneUIDFrame, EddystoneURLFrame, EddystoneEncryptedTLMFrame, \
                          EddystoneTLMFrame
from .const import EDDYSTONE_TLM_UNENCRYPTED, EDDYSTONE_TLM_ENCRYPTED, SERVICE_DATA_TYPE, \
                   EDDYSTONE_UID_FRAME, EDDYSTONE_TLM_FRAME, EDDYSTONE_URL_FRAME


def parse_packet(packet):
    """Parse a beacon advertisement packet."""
    try:
        frame = EddystoneFrame.parse(packet)
        for tlv in frame:
            if tlv['type'] == SERVICE_DATA_TYPE:
                data = tlv['value']
                if data['frame_type'] == EDDYSTONE_UID_FRAME:
                    return EddystoneUIDFrame(data['frame'])

                elif data['frame_type'] == EDDYSTONE_TLM_FRAME:
                    if data['frame']['tlm_version'] == EDDYSTONE_TLM_ENCRYPTED:
                        return EddystoneEncryptedTLMFrame(data['frame']['data'])
                    elif data['frame']['tlm_version'] == EDDYSTONE_TLM_UNENCRYPTED:
                        return EddystoneTLMFrame(data['frame']['data'])

                elif data['frame_type'] == EDDYSTONE_URL_FRAME:
                    return EddystoneURLFrame(data['frame'])

    except ConstructError:
        traceback.print_exc()
        return None

    return None
