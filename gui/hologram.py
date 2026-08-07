"""
Advanced Holographic Core Visualization for Ultron
Creates fluid, smooth 3D holographic display inspired by Iron Man
Uses advanced 3D projection and organic animations
"""

import tkinter as tk
from tkinter import Canvas
import math
import numpy as np
from typing import List, Tuple, Dict
import time

class Point3D:
    """3D point representation"""
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def rotate_x(self, angle: float):
        """Rotate around X axis"""
        rad = math.radians(angle)
        y = self.y * math.cos(rad) - self.z * math.sin(rad)
        z = self.y * math.sin(rad) + self.z * math.cos(rad)
        return Point3D(self.x, y, z)
    
    def rotate_y(self, angle: float):
        """Rotate around Y axis"""
        rad = math.radians(angle)
        x = self.x * math.cos(rad) + self.z * math.sin(rad)
        z = -self.x * math.sin(rad) + self.z * math.cos(rad)
        return Point3D(x, self.y, z)
    
    def rotate_z(self, angle: float):
        """Rotate around Z axis"""
        rad = math.radians(angle)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) + self.y * math.cos(rad)
        return Point3D(x, y, self.z)
    
    def project_2d(self, center_x: float, center_y: float, scale: float = 100) -> Tuple[float, float]:
        """Project 3D point to 2D screen coordinates"""
        # Perspective projection
        perspective = 1 / (1 + self.z / 500)
        x_2d = center_x + self.x * perspective * scale
        y_2d = center_y + self.y * perspective * scale
        return x_2d, y_2d, perspective


class HologramMesh:
    """3D mesh for holographic core"""
    
    def __init__(self, mesh_type: str = "icosphere"):
        self.vertices = []
        self.faces = []
        self.mesh_type = mesh_type
        
        if mesh_type == "icosphere":
            self.create_icosphere()
        elif mesh_type == "cube":
            self.create_cube()
        elif mesh_type == "torus":
            self.create_torus()
    
    def create_icosphere(self, subdivisions: int = 2):
        """Create icosphere (sphere-like polyhedron)"""
        phi = (1 + math.sqrt(5)) / 2
        
        # Initial vertices
        vertices = [
            [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
            [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
            [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
        ]
        
        # Normalize vertices
        for v in vertices:
            length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
            v[0] /= length
            v[1] /= length
            v[2] /= length
        
        self.vertices = vertices
    
    def create_cube(self):
        """Create cube mesh"""
        s = 1
        self.vertices = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
        ]
    
    def create_torus(self, major_radius: float = 1.0, minor_radius: float = 0.3, segments: int = 20):
        """Create torus mesh"""
        self.vertices = []
        
        for i in range(segments):
            theta = (2 * math.pi * i) / segments
            for j in range(segments):
                phi = (2 * math.pi * j) / segments
                
                x = (major_radius + minor_radius * math.cos(phi)) * math.cos(theta)
                y = minor_radius * math.sin(phi)
                z = (major_radius + minor_radius * math.cos(phi)) * math.sin(theta)
                
                self.vertices.append([x, y, z])


class AdvancedHologram:
    """Advanced holographic core with smooth 3D animations"""
    
    def __init__(self, canvas: Canvas, config):
        self.canvas = canvas
        self.config = config
        self.center_x = canvas.winfo_width() / 2
        self.center_y = canvas.winfo_height() / 2
        
        # 3D meshes
        self.core_mesh = HologramMesh("icosphere")
        self.ring_mesh = HologramMesh("torus")
        self.inner_mesh = HologramMesh("cube")
        
        # Animation parameters
        self.time = 0
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.pulse = 0
        self.is_animating = True
        self.animation_speed = 1.0
        self.response_intensity = 0.5
        
        # Particle systems
        self.particles = self.create_particle_system(150)
        self.energy_waves = self.create_energy_waves()
        
        # Color system
        self.base_color = config.HOLOGRAM_COLOR
        self.color_intensity = 1.0
        
        # Performance optimization
        self.last_frame_time = time.time()
        self.fps = 0
    
    def create_particle_system(self, num_particles: int) -> List[Dict]:
        """Create particle system with smooth motion"""
        particles = []
        for i in range(num_particles):
            particles.append({
                "x": np.random.uniform(-2, 2),
                "y": np.random.uniform(-2, 2),
                "z": np.random.uniform(-2, 2),
                "vx": np.random.uniform(-0.05, 0.05),
                "vy": np.random.uniform(-0.05, 0.05),
                "vz": np.random.uniform(-0.05, 0.05),
                "life": np.random.uniform(0.5, 2.0),
                "max_life": np.random.uniform(0.5, 2.0),
                "size": np.random.uniform(1, 4)
            })
        return particles
    
    def create_energy_waves(self) -> List[Dict]:
        """Create energy wave effects"""
        return [
            {"radius": 0, "life": 0, "intensity": 0},
            {"radius": 0, "life": 0, "intensity": 0},
            {"radius": 0, "life": 0, "intensity": 0}
        ]
    
    def update_particles(self, dt: float):
        """Update particle positions with smooth motion"""
        for particle in self.particles:
            # Update position
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["z"] += particle["vz"]
            
            # Life decay
            particle["life"] -= dt * 0.5
            
            # Respawn when life ends
            if particle["life"] <= 0:
                particle["x"] = np.random.uniform(-2, 2)
                particle["y"] = np.random.uniform(-2, 2)
                particle["z"] = np.random.uniform(-2, 2)
                particle["vx"] = np.random.uniform(-0.05, 0.05)
                particle["vy"] = np.random.uniform(-0.05, 0.05)
                particle["vz"] = np.random.uniform(-0.05, 0.05)
                particle["life"] = particle["max_life"]
            
            # Add some gravity toward center
            distance = math.sqrt(particle["x"]**2 + particle["y"]**2 + particle["z"]**2)
            if distance > 0:
                pull = 0.02 * self.animation_speed
                particle["vx"] -= (particle["x"] / distance) * pull
                particle["vy"] -= (particle["y"] / distance) * pull
                particle["vz"] -= (particle["z"] / distance) * pull
    
    def update_energy_waves(self, dt: float):
        """Update energy wave animations"""
        for wave in self.energy_waves:
            wave["radius"] += 0.08 * self.animation_speed
            wave["life"] -= dt
            
            if wave["radius"] > 3:
                wave["radius"] = 0
                wave["life"] = 1.0
                wave["intensity"] = self.response_intensity
    
    def draw_frame(self):
        """Draw single animation frame"""
        if not self.is_animating:
            return
        
        # Calculate delta time
        current_time = time.time()
        dt = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Clear canvas
        self.canvas.delete("hologram")
        
        # Update animation time
        self.time += dt * self.animation_speed
        
        # Smooth, organic rotations (sine/cosine based)
        self.rotation_x = math.sin(self.time * 0.5) * 30
        self.rotation_y = self.time * 20 * self.animation_speed
        self.rotation_z = math.cos(self.time * 0.3) * 15
        
        # Smooth pulse effect
        self.pulse = 1.0 + 0.3 * math.sin(self.time * 2) + 0.2 * self.response_intensity
        self.color_intensity = 0.8 + 0.2 * math.sin(self.time * 1.5)
        
        # Draw components in order of depth
        self.draw_energy_waves()
        self.update_particles(dt)
        self.draw_particle_system()
        self.draw_rotating_rings()
        self.draw_core_mesh()
        self.draw_inner_glow()
        self.draw_data_streams()
        
        # Update waves
        self.update_energy_waves(dt)
        
        # Draw info (optional)
        # self.draw_fps(current_time)
    
    def draw_core_mesh(self):
        """Draw the main 3D core mesh with smooth shading"""
        projected_points = []
        
        for vertex in self.core_mesh.vertices:
            point = Point3D(vertex[0], vertex[1], vertex[2])
            
            # Apply rotations
            point = point.rotate_x(self.rotation_x)
            point = point.rotate_y(self.rotation_y)
            point = point.rotate_z(self.rotation_z)
            
            # Scale with pulse
            scale = 0.5 * self.pulse
            x2d, y2d, perspective = point.project_2d(self.center_x, self.center_y, scale * 100)
            
            # Calculate brightness based on normal direction (Lambertian shading)
            brightness = max(0.3, (point.z + 1) / 2)
            brightness *= perspective
            brightness = min(1.0, brightness * 1.5)
            
            color = self.get_color_with_intensity(brightness * self.color_intensity)
            projected_points.append((x2d, y2d, perspective, color))
        
        # Draw edges
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]
        
        for edge in edges:
            p1 = projected_points[edge[0]]
            p2 = projected_points[edge[1]]
            
            self.canvas.create_line(
                p1[0], p1[1], p2[0], p2[1],
                fill=p1[3],
                width=2,
                smooth=True,
                tags="hologram"
            )
    
    def draw_rotating_rings(self):
        """Draw smooth rotating rings"""
        num_rings = 4
        
        for ring_idx in range(num_rings):
            ring_radius = (ring_idx + 1) * 0.3 * self.pulse
            segments = 100
            
            # Create smooth ring path
            points = []
            for i in range(segments):
                angle = (2 * math.pi * i) / segments
                
                # Add wave motion to rings
                wave = math.sin(angle * 3 + self.time * 2) * 0.1
                
                x = (ring_radius + wave) * math.cos(angle)
                y = ring_radius * math.sin(angle) * 0.5
                z = (ring_radius + wave) * math.sin(angle)
                
                point = Point3D(x, y, z)
                point = point.rotate_y(self.rotation_y + ring_idx * 30)
                
                x2d, y2d, _ = point.project_2d(self.center_x, self.center_y, 100)
                points.append((x2d, y2d))
            
            # Draw smooth curve
            if len(points) > 1:
                flat_points = [coord for point in points for coord in point]
                
                # Calculate color based on ring intensity
                ring_intensity = self.color_intensity * (1.0 - ring_idx * 0.15)
                color = self.get_color_with_intensity(ring_intensity)
                
                try:
                    self.canvas.create_line(
                        *flat_points,
                        fill=color,
                        width=1.5,
                        smooth=True,
                        tags="hologram"
                    )
                except:
                    pass
    
    def draw_particle_system(self):
        """Draw smooth particle effects"""
        for particle in self.particles:
            if particle["life"] <= 0:
                continue
            
            point = Point3D(
                particle["x"] * 0.5,
                particle["y"] * 0.5,
                particle["z"] * 0.5
            )
            
            point = point.rotate_y(self.rotation_y)
            x2d, y2d, perspective = point.project_2d(self.center_x, self.center_y, 100)
            
            # Particle life-based opacity and size
            life_ratio = particle["life"] / particle["max_life"]
            size = particle["size"] * (life_ratio ** 0.5)
            
            # Color intensity based on life
            intensity = self.color_intensity * life_ratio * perspective
            color = self.get_color_with_intensity(intensity)
            
            self.canvas.create_oval(
                x2d - size, y2d - size,
                x2d + size, y2d + size,
                fill=color,
                outline=color,
                tags="hologram"
            )
    
    def draw_energy_waves(self):
        """Draw expanding energy waves"""
        for wave in self.energy_waves:
            if wave["life"] <= 0:
                continue
            
            wave_radius = wave["radius"] * self.pulse * 100
            alpha = wave["life"] * wave["intensity"]
            
            color = self.get_color_with_intensity(alpha * 0.7)
            
            try:
                self.canvas.create_oval(
                    self.center_x - wave_radius,
                    self.center_y - wave_radius,
                    self.center_x + wave_radius,
                    self.center_y + wave_radius,
                    outline=color,
                    width=1,
                    tags="hologram"
                )
            except:
                pass
    
    def draw_inner_glow(self):
        """Draw smooth inner glow effect"""
        if self.config.CORE_GLOW_EFFECT:
            glow_radius = 0.15 * self.pulse * 100
            glow_intensity = 0.5 + 0.5 * math.sin(self.time * 3)
            
            color = self.get_color_with_intensity(glow_intensity * self.color_intensity)
            
            self.canvas.create_oval(
                self.center_x - glow_radius,
                self.center_y - glow_radius,
                self.center_x + glow_radius,
                self.center_y + glow_radius,
                fill=color,
                outline=color,
                tags="hologram"
            )
    
    def draw_data_streams(self):
        """Draw flowing data stream lines"""
        num_streams = 5
        
        for stream_idx in range(num_streams):
            stream_angle = (2 * math.pi * stream_idx) / num_streams
            stream_points = []
            
            for i in range(30):
                progress = i / 30
                angle = stream_angle + (self.time * 2 + progress * math.pi)
                
                # Spiral motion
                radius = 0.3 + progress * 0.5
                height = math.sin(progress * math.pi * 2 + self.time) * 0.3
                
                x = radius * math.cos(angle)
                y = height
                z = radius * math.sin(angle)
                
                point = Point3D(x, y, z)
                x2d, y2d, perspective = point.project_2d(self.center_x, self.center_y, 100)
                
                intensity = perspective * (1 - progress)
                stream_points.append((x2d, y2d, intensity))
            
            # Draw stream segments
            for i in range(len(stream_points) - 1):
                x1, y1, intensity1 = stream_points[i]
                x2, y2, intensity2 = stream_points[i + 1]
                
                avg_intensity = (intensity1 + intensity2) / 2
                color = self.get_color_with_intensity(avg_intensity * 0.6)
                
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color,
                    width=1,
                    tags="hologram"
                )
    
    def get_color_with_intensity(self, intensity: float) -> str:
        """Generate neon green color with intensity"""
        intensity = max(0, min(1, intensity))
        
        # Neon green (#00FF00) with intensity modulation
        r = int(0 + intensity * 50)
        g = int(100 + intensity * 155)
        b = int(0 + intensity * 100)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def set_response_mode(self, intensity: float = 0.8):
        """Set to response mode with high intensity"""
        self.response_intensity = max(0, min(1, intensity))
        self.animation_speed = 1.0 + intensity
    
    def set_idle_mode(self):
        """Set to idle mode with calm animation"""
        self.response_intensity = 0.3
        self.animation_speed = 1.0
    
    def start(self):
        """Start animation"""
        self.is_animating = True
    
    def stop(self):
        """Stop animation"""
        self.is_animating = False
        self.canvas.delete("hologram")


class AdvancedHologramDisplay:
    """Main hologram display window"""
    
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.root.title("ULTRON - Advanced Holographic Interface")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)
        
        # Create canvas with high quality
        self.canvas = Canvas(
            self.root,
            bg="#000000",
            highlightthickness=0,
            cursor="crosshair",
            bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create hologram
        self.hologram = AdvancedHologram(self.canvas, config)
        
        # Animation control
        self.animating = True
        self.animate()
        
        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Handle window resize"""
        self.hologram.center_x = event.width / 2
        self.hologram.center_y = event.height / 2
    
    def animate(self):
        """Animation loop"""
        if self.animating:
            self.hologram.draw_frame()
            self.root.after(16, self.animate)  # ~60 FPS
    
    def update_response(self, response: str, intensity: float = 0.8):
        """React to AI response"""
        self.hologram.set_response_mode(intensity)
    
    def idle(self):
        """Go to idle state"""
        self.hologram.set_idle_mode()
    
    def run(self):
        """Run display"""
        self.root.mainloop()
    
    def close(self):
        """Close display"""
        self.animating = False
        self.hologram.stop()
        self.root.quit()
