# Michelaingelo

A 3D stone carving machine for shaping stone, marble, and other suitable carving materials.

The goal is to combine scanning and carving around a central circular platform. The motion concept is similar to a 360° spin camera booth: an actuator beneath the platform moves a robotic arm around the material being worked on.

## Machine concept

- **Central platform:** the user places the stone on a circular base in the middle of the machine. The stone stays in place while the arm travels around it.
- **Orbital drive:** an actuator beneath the base drives the mechanism that carries the arm around the platform.
- **Robotic arm:** positions the scanning equipment and carving head relative to the stone.
- **Cameras and sensors:** mounted on the arm to scan the stone and capture its shape.
- **Modular carving head:** mounted at the tip of the arm. The user can change the tool, choosing finer or thicker tools to produce different details and finishes.

The intended workflow is to place and secure the material, scan its geometry, plan the carving, and remove material with the selected tool. Tool changes allow different stages of shaping and detail work.

## Current CAD model

This is an early concept project. The SolidCraft model currently contains only the circular base.

| Property | Current model |
| --- | --- |
| Shape | Solid circular disk with flat top and bottom |
| Diameter | 450 mm / 45 cm |
| Thickness | 10 mm / 1 cm |
| Position | Centered on the origin, with its bottom on the XY plane |
| Feature and body name | Sculpture base |

These dimensions describe the modeled geometry. The base material, load capacity, and workholding are still to be designed. The actuator, orbiting mechanism, robotic arm, scanning equipment, and tool head have not yet been modeled.

## Design questions

- Maximum stone dimensions and mass, and how the stone is secured.
- Bearing arrangement, actuator, and transmission for the orbital motion beneath the base.
- Arm reach, joints, range of motion, and stiffness during carving.
- Tool head mounting interface, tool drive, and supported tool sizes.
- Camera and sensor placement, calibration, and the relationship between scan coordinates and tool motion.
- Software for scanning, carving plans, toolpaths, and machine control.

## Project files

- `michelaingelo.sc` — native SolidCraft model.
- `README.md` — project concept, current geometry, and open design questions.
- `.gitignore` — excludes local system files, SolidCraft locks, and backup files.
- `.gitattributes` — treats SolidCraft containers as binary files in Git.

## Working on the project

Open `michelaingelo.sc` in SolidCraft. Use SolidCraft's MCP for CAD changes, and save the native model back into this directory. Model dimensions are in millimetres.

Keep this README aligned with the model as the machine develops, distinguishing the planned machine from components already modeled.
