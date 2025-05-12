#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/chenfeng',
    'hardware/qcom-caf/wlan',
    'hardware/qcom-caf/sm8650',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.diaghal@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.ImsRtpService-V1-ndk'
    ): lib_fixup_vendor_suffix,
    (
        'android.hardware.graphics.allocator-V1-ndk',
        'android.hardware.graphics.composer3-V2-ndk',
        'audio.primary.pineapple',
        'libmilut',
        'libmips',
        'libmisr',
        'libagmclient',
        'libagmmixer',
        'libpalclient',
        'libwpa_client',
        'vendor.qti.hardware.display.composer3-V1-ndk',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/hw/vendor.qti.media.c2@1.0-service',
        'vendor/bin/hw/vendor.dolby.media.c2@1.0-service',
        'vendor/bin/hw/vendor.qti.media.c2audio@1.0-service'
    ): blob_fixup()
        .add_needed('libshim.so'),
    'vendor/etc/sensors/hals.conf': blob_fixup()
        .add_line_if_missing('sensors.xiaomi.v2.so'),
    (
        'odm/etc/camera/enhance_motiontuning.xml',
        'odm/etc/camera/night_motiontuning.xml',
        'odm/etc/camera/motiontuning.xml'
    ): blob_fixup()
        .regex_replace('xml=version', 'xml version'),
    (
        'odm/lib64/libcamxcommonutils.so',
        'vendor/lib64/libcameraopt.so',
        'odm/lib64/hw/camera.qcom.so'
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'vendor/etc/media_codecs_pinaepple.xml', 
        'vendor/etc/media_codecs_pinaepple_vendor.xml'
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
        'odm/lib64/camera/plugins/com.xiaomi.plugin.jpegrAggr.so'
    ): blob_fixup()
        .add_needed('libcamerahdr_shim.so'),
    (
        'odm/lib64/com.qti.qseeaon.so'
    ): blob_fixup()
        .add_needed('libcameraflare_shim.so'),
    (
        'odm/lib64/camera/plugins/com.xiaomi.plugin.gainmap.so'
    ): blob_fixup()
        .add_needed('libcameraplugin_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'chenfeng',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
    add_firmware_proprietary_file=True
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
