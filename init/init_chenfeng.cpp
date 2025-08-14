/*
     Copyright (C) 2024 The LineageOS Project
     SPDX-License-Identifier: Apache-2.0
 */

#include <vector>
#include <android-base/properties.h>
#define _REALLY_INCLUDE_SYS__SYSTEM_PROPERTIES_H_
#include <sys/_system_properties.h>

using android::base::GetProperty;

std::vector<std::string> ro_props_default_source_order = {
    "",
    "bootimage.",
    "odm.",
    "odm_dlkm.",
    "product.",
    "system.",
    "system_ext.",
    "vendor.",
    "vendor_dlkm.",
};

void property_override(char const prop[], char const value[], bool add = true) {
    prop_info *pi;
    pi = (prop_info *) __system_property_find(prop);
    if (pi)
        __system_property_update(pi, value, strlen(value));
    else if (add)
        __system_property_add(prop, strlen(prop), value, strlen(value));
}

void set_ro_build_prop(const std::string &prop, const std::string &value) {
    for (const auto &source : ro_props_default_source_order) {
        auto prop_name = "ro." + source + "build." + prop;
        if (source == "")
            property_override(prop_name.c_str(), value.c_str());
        else
            property_override(prop_name.c_str(), value.c_str(), false);
    }
}

void set_ro_product_prop(const std::string &prop, const std::string &value) {
    for (const auto &source : ro_props_default_source_order) {
        auto prop_name = "ro.product." + source + prop;
        property_override(prop_name.c_str(), value.c_str(), false);
    }
}

void vendor_load_properties() {
    std::string region;
    std::string sku;
    std::string hwversion;
    region = GetProperty("ro.boot.hwc", "");
    sku = GetProperty("ro.boot.hardware.sku", "");
    hwversion = GetProperty("ro.boot.hwversion", "");

    std::string model;
    std::string brand;
    std::string device;
    std::string fingerprint;
    std::string description;
    std::string marketname;
    std::string mod_device = "chenfeng_global"; // Default mod_device

    if (region == "CN") {
        device = "chenfeng";
        brand = "Xiaomi";
        description = "chenfeng_global-user 15 AQ3A.240912.001 OS2.0.105.0.VNJCNXM release-keys";
        fingerprint = "Xiaomi/chenfeng_global/chenfeng:15/AQ3A.240912.001/OS2.0.100.0.VNPMIXM:user/release-keys";
        marketname = "Xiaomi Civi 4 Pro";
        model = "24053PY09C";
    } else if (region == "IN") {
        device = "chenfeng";
        brand = "Xiaomi";
        description = "chenfeng-user 15 AQ3A.240912.001 OS2.0.102.0.VNJINXM release-keys";
        fingerprint = "Xiaomi/chenfeng/chenfeng:15/AQ3A.240912.001/OS2.0.102.0.VNJINXM:user/release-keys";
        marketname = "Xiaomi Civi 14 Pro";
        model = "24053PY09I";
    }

    set_ro_build_prop("fingerprint", fingerprint);
    set_ro_product_prop("brand", brand);
    set_ro_product_prop("device", device);
    set_ro_product_prop("model", model);
    
    property_override("ro.product.marketname", marketname.c_str());
    property_override("ro.build.description", description.c_str());
    if (!mod_device.empty()) {
        property_override("ro.product.mod_device", mod_device.c_str());
    }
}
