// MYLLÄRI Beer Tap Handle - Complete 3D Design
// For Bambu Lab 3D Printing
// 
// Usage: Open in OpenSCAD, then File > Export > Export as STL

// ==================== DIMENSIONS ====================

// Top Disk (Badge) - for flavor logo
disk_diameter = 80;
disk_thickness = 8;

// Text Pillar (Shaft)
shaft_height = 155;
shaft_width = 48;
shaft_thickness = 30;
text_depth = 1.2;  // How much text protrudes

// Transition (Neck)
neck_height = 10;

// Nut Base (with M10 nut recess)
base_height = 35;
base_diameter = 35;
m10_nut_outer = 17;  // M10 hex nut width across flats
m10_nut_inner = 10;   // M10 thread inner diameter
nut_hole_depth = 8;

// Keyway (Anti-rotation)
keyway_width = 20;
keyway_depth = 5;

// Fillet
fillet = 2;

// ==================== MODULES ====================

module rounded_box(w, h, d, r) {
    // Box with rounded edges
    hull() {
        // 8 corners
        translate([w/2 - r, h/2 - r, d/2 - r]) sphere(r);
        translate([w/2 - r, -(h/2 - r), d/2 - r]) sphere(r);
        translate([-(w/2 - r), h/2 - r, d/2 - r]) sphere(r);
        translate([-(w/2 - r), -(h/2 - r), d/2 - r]) sphere(r);
        translate([w/2 - r, h/2 - r, -(d/2 - r)]) sphere(r);
        translate([w/2 - r, -(h/2 - r), -(d/2 - r)]) sphere(r);
        translate([-(w/2 - r), h/2 - r, -(d/2 - r)]) sphere(r);
        translate([-(w/2 - r), -(h/2 - r), -(d/2 - r)]) sphere(r);
    }
}

module hex_nut(size, height) {
    // Hexagon nut
    cylinder(r = size * 0.58, h = height, $fn = 6, center = true);
}

module text_extruded(message, size, depth) {
    // Extruded 3D text
    linear_extrude(height = depth, convexity = 5) {
        text(message, size = size, font = "Helvetica:style=Bold", 
             halign = "center", valign = "center");
    }
}

// ==================== MAIN TAP HANDLE ====================

module tap_handle_base() {
    // === BASE (Nut Mount) ===
    translate([0, 0, base_height/2]) {
        // Main cylinder
        cylinder(r = base_diameter/2, h = base_height, center = true);
        
        // Hex nut recess (from bottom)
        translate([0, 0, -base_height/2 + 1]) {
            difference() {
                hex_nut(m10_nut_outer, nut_hole_depth + 2);
                // Inner thread hole
                cylinder(r = m10_nut_inner/2, h = nut_hole_depth + 4, center = true);
            }
        }
    }
    
    // === NECK (Transition) ===
    translate([0, 0, base_height + neck_height/2]) {
        // Smooth transition from rectangle to circle
        linear_extrude(height = neck_height, convexity = 4) {
            hull() {
                square([shaft_width - fillet*2, shaft_thickness - fillet*2], center = true);
                circle(r = base_diameter/2 - fillet);
            }
        }
    }
    
    // === SHAFT (Main Pillar) ===
    translate([0, 0, base_height + neck_height + shaft_height/2]) {
        // Main pillar
        rounded_box(shaft_width - fillet*2, shaft_thickness - fillet*2, shaft_height - fillet*2, fillet);
        
        // MYLLÄRI Text - Vertical on front face
        // Text runs bottom to top
        translate([0, shaft_thickness/2 + text_depth/2, 0]) {
            // Rotate text to be vertical
            rotate([0, 0, 90]) {
                // Each letter positioned vertically
                // M
                translate([0, -50, 0]) text_extruded("M", 22, text_depth);
                // Y
                translate([0, -30, 0]) text_extruded("Y", 22, text_depth);
                // L
                translate([0, -10, 0]) text_extruded("L", 22, text_depth);
                // L
                translate([0, 10, 0]) text_extruded("L", 22, text_depth);
                // Ä
                translate([0, 30, 0]) text_extruded("Ä", 22, text_depth);
                // R
                translate([0, 50, 0]) text_extruded("R", 22, text_depth);
                // I
                translate([0, 70, 0]) text_extruded("I", 22, text_depth);
            }
        }
    }
    
    // === KEYWAY (Anti-rotation slot) ===
    translate([0, 0, base_height + neck_height + shaft_height + keyway_depth/2]) {
        cube([keyway_width, shaft_thickness, keyway_depth], center = true);
    }
}

module top_disk(flavor_name = "MIAMI NEIPA", abv = "5.5%") {
    total_height = base_height + neck_height + shaft_height;
    
    translate([0, 0, total_height + disk_thickness/2]) {
        // Main disk
        difference() {
            cylinder(r = disk_diameter/2, h = disk_thickness, center = true);
            // Center screw hole
            cylinder(r = 4, h = disk_thickness + 2, center = true);
        }
        
        // Connection protrusion (fits into keyway)
        translate([0, 0, -disk_thickness/2]) {
            cube([keyway_width - 0.3, keyway_width - 0.3, 4], center = true);
        }
        
        // Flavor name circle (embossed area)
        translate([0, 0, -disk_thickness/2 - 0.5]) {
            difference() {
                cylinder(r = disk_diameter/2 - 12, h = 1.5, center = true);
                cylinder(r = disk_diameter/2 - 18, h = 3, center = true);
            }
        }
        
        // Flavor text (inside the circle)
        translate([0, 0, -disk_thickness/2 - 0.8]) {
            rotate([0, 0, 0]) {
                // Flavor name
                linear_extrude(height = 1, convexity = 5) {
                    text(flavor_name, size = 10, font = "Helvetica:style=Bold",
                         halign = "center", valign = "center");
                }
                // ABV
                translate([0, -10, 0]) {
                    linear_extrude(height = 1, convexity = 5) {
                        text(abv, size = 8, font = "Helvetica",
                             halign = "center", valign = "center");
                    }
                }
            }
        }
    }
}

// ==================== RENDER ====================

// Show base + shaft
tap_handle_base();

// Show top disk (flavor)
top_disk("MIAMI NEIPA", "5.5%");

// Optional: Show exploded view
// translate([0, 80, 0]) tap_handle_base();
// translate([0, -80, 0]) top_disk();
