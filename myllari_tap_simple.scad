// MYLLÄRI Beer Tap Handle - Simple Version
// For Bambu Lab 3D Printing
// This version works without font dependencies

// Dimensions
disk_d = 80;
disk_t = 8;
shaft_h = 155;
shaft_w = 48;
shaft_t = 30;
neck_h = 10;
base_h = 35;
base_d = 35;
keyway_w = 20;
keyway_d = 5;

// Base
translate([0, 0, base_h/2]) {
    cylinder(r = base_d/2, h = base_h, center=true);
    // Nut hole
    translate([0, 0, -base_h/2+3]) cylinder(r=5, h=8, center=true);
}

// Neck
translate([0, 0, base_h + neck_h/2]) {
    linear_extrude(height=neck_h) hull() {
        square([shaft_w-4, shaft_t-4], center=true);
        circle(r=base_d/2-2);
    }
}

// Shaft
translate([0, 0, base_h + neck_h + shaft_h/2]) {
    cube([shaft_w, shaft_t, shaft_h], center=true);
}

// Keyway slot
translate([0, 0, base_h + neck_h + shaft_h + keyway_d/2]) {
    cube([keyway_w, shaft_t, keyway_d], center=true);
}

// Top Disk
translate([0, 0, base_h + neck_h + shaft_h + disk_t/2]) {
    cylinder(r=disk_d/2, h=disk_t, center=true);
    cylinder(r=4, h=disk_t+2, center=true); // screw hole
    // Protrusion
    translate([0, 0, -disk_t/2]) cube([keyway_w-0.3, keyway_w-0.3, 4], center=true);
    // Flavor circle
    translate([0, 0, -disk_t/2-0.5]) difference() {
        cylinder(r=disk_d/2-12, h=1.5, center=true);
        cylinder(r=disk_d/2-18, h=3, center=true);
    }
}
