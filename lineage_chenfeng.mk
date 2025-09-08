#
# Copyright (C) 2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit some common LineageOS stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit from chenfeng device
$(call inherit-product, device/xiaomi/chenfeng/device.mk)

PRODUCT_NAME := lineage_chenfeng
PRODUCT_DEVICE := chenfeng
PRODUCT_MANUFACTURER := Xiaomi
PRODUCT_BRAND := POCO
PRODUCT_MODEL := 24053PY09I

# Device-identify
TARGET_HAS_UDFPS := true

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="chenfeng_global-user 15 AQ3A.240912.001 OS2.0.105.0.VNJCNXM release-keys" \
    BuildFingerprint=POCO/chenfeng_global/chenfeng:15/AQ3A.240912.001/OS2.0.105.0.VNJCNXM:user/release-keys \
    DeviceName=chenfeng
    DeviceProduct=chenfeng_global \
    SystemName=chenfeng_global \
    SystemDevice=chenfeng

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

