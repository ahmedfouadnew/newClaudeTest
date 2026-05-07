FRC_SEASONS = {
    "2025": {
        "name": "Reefscape",
        "year": 2025,
        "type": "FRC",
        "context": """
FRC 2025 REEFSCAPE — Season Overview
=====================================
Game: Reefscape (ocean/coral reef theme)
Field: Two alliances (red/blue) of 3 robots each.

SCORING ELEMENTS:
- Coral: game pieces placed on the Reef structure at 4 levels (L1–L4). Higher levels = more points.
- Algae: game pieces removed from the Reef and scored in the Processor or Barge net.

KEY FIELD ELEMENTS:
- Reef: central structure with branches for Coral placement; has algae on alternating branches.
- Processor: alliance-specific scoring zone for Algae.
- Barge: large net structure; Algae thrown in = points; robots can climb Barge in endgame.
- Coral Station: human player loading stations on driver station wall.

MATCH PHASES:
- Auto (15s): robots act autonomously. Leaving starting zone = 3pts. Coral/Algae scored = bonus points.
- Teleop (2m15s): driver-controlled play.
- Endgame (last 30s of teleop): robots can park on Barge or climb (shallow/deep) for bonus points.

ENDGAME CLIMB:
- Park: 2 pts
- Shallow Cage: 6 pts
- Deep Cage: 12 pts

CORAL POINTS (Teleop):
- L1: 2 pts, L2: 3 pts, L3: 4 pts, L4: 5 pts

RANKING POINTS (RP): Win=2, Tie=1, Loss=0. Bonus RPs for Coopertition (Algae in Processor) and completing the Reef.

COMMON MECHANISMS:
- Coral intake: ground intake or human-player station intake; coral is a hollow torus shape.
- Elevator/arm: needed to reach L3–L4 coral branches (~6 ft high).
- Algae removal: spinning roller or fork to knock algae off reef.
- Climb: hook-and-winch, telescoping arms, or passive hooks for Barge cage.

PROGRAMMING NOTES:
- Auto paths must navigate around/through Reef; PathPlanner or Choreo commonly used.
- Vision (Limelight/PhotonVision) with AprilTags for alignment to Reef branches.
- Pose estimation critical for consistent auto and semi-auto driver assists.
""",
    },
    "2024": {
        "name": "Crescendo",
        "year": 2024,
        "type": "FRC",
        "context": """
FRC 2024 CRESCENDO — Season Overview
======================================
Game: Crescendo (music theme)
Field: Two alliances (red/blue) of 3 robots each.

SCORING ELEMENTS:
- Notes: foam ring game pieces, scored in Speaker or Amp.

KEY FIELD ELEMENTS:
- Speaker: high goal above alliance wall; Notes shot in = 2pts (teleop), 5pts (amplified).
- Amp: lower side goal; Notes scored = 1pt; used to amplify Speaker.
- Stage: three-legged structure in center; robots climb chains in endgame.
- Source: human player loading on opponent side.

MATCH PHASES:
- Auto (15s): Leave starting zone = 2pts. Notes preloaded or picked from Wing.
- Teleop (2m15s): driver play.
- Endgame (last 20s): Trap (Note in Stage trap = 5pts), Climb (Onstage = 3pts, Harmony +2 per extra bot), Spotlight (chain lit = 1pt each).

RANKING POINTS: Ensemble RP (climb), Melody RP (Note count threshold).

COMMON MECHANISMS:
- Ground intake: compliant wheels or belts to pick up Notes from floor.
- Shooter: flywheel shooter (angled) to score in Speaker; requires tuned velocity + hood angle.
- Amp scorer: separate path or pivot to score in Amp at lower angle.
- Climber: hook and winch or telescoping arms for Stage chains.

PROGRAMMING NOTES:
- Shooter tuning: interpolation table (distance → RPM + angle) using Limelight targeting Speaker AprilTags.
- Auto routines commonly use 2–5 Note paths.
- Swerve drive dominant this season; WPILib SwerveControllerCommand or CTRE/REV swerve libraries.
""",
    },
    "2023": {
        "name": "Charged Up",
        "year": 2023,
        "type": "FRC",
        "context": """
FRC 2023 CHARGED UP — Season Overview
=======================================
Game: Charged Up (electrical/energy theme)
Field: Two alliances of 3 robots.

SCORING ELEMENTS:
- Cones: orange traffic-cone shaped pieces.
- Cubes: purple foam cubes.

KEY FIELD ELEMENTS:
- Grid: 3x9 node scoring structure. Top row = Cone only. Middle row = Cone only. Bottom row = Hybrid (cone or cube). Cube nodes in specific columns.
- Charging Station: seesaw-like platform in center; robots balance for endgame.
- Substation: human player loading on alliance wall (single or double).

MATCH PHASES:
- Auto (15s): Mobility (leave community) = 3pts. Scoring + Charging Station Engaged = bonus RP.
- Teleop: place game pieces on Grid.
- Endgame: Dock (on platform) = 6pts, Engage (balanced) = 10pts.

RANKING POINTS: Sustainability RP (charge station), Activation RP (all links on grid).

COMMON MECHANISMS:
- Single-jointed or double-jointed arm for reaching top row (~6ft).
- Wrist + claw end effector to handle both cones (vertical) and cubes.
- Ground intake vs. human player station intake strategies.
- Auto-balance PID on Charging Station.

PROGRAMMING NOTES:
- Auto-balance: gyro-based PID or bang-bang on Charging Station pitch angle.
- AprilTag vision for Grid alignment; often combined with retroreflective tape targeting.
""",
    },
}

FTC_SEASONS = {
    "2024": {
        "name": "Into The Deep",
        "year": 2024,
        "type": "FTC",
        "context": """
FTC 2024-25 INTO THE DEEP — Season Overview
=============================================
Game: Into The Deep (underwater theme)
Field: 12x12 ft field, two alliances of 2 robots each.

SCORING ELEMENTS:
- Samples: small yellow/blue/red colored block-shaped game pieces.
- Specimens: sample + clip combination, scored on chamber.

KEY FIELD ELEMENTS:
- Net Zone: angled net on each alliance wall; samples tossed in = points.
- Observation Zone: area near human player for specimen preparation.
- Submersible: central structure with bars for hanging; specimens clipped onto bars.
- Baskets: high/low baskets for sample scoring.

MATCH PHASES:
- Auto (30s): Autonomous. Park in Observation Zone, score samples/specimens.
- Teleop (2m): driver play.
- Endgame (last 30s): Hang on Submersible bars (low = 3pts, high = 15pts), or park (3pts).

SPECIMEN SCORING: Clip specimen onto chamber bars (high = 10pts, low = 5pts).
SAMPLE SCORING: Net Zone = 2pts; High Basket = 8pts; Low Basket = 4pts.

COMMON MECHANISMS:
- Ground intake: claw or scooping mechanism for picking up samples.
- Linear slide or arm: reach high basket (~32 inches off ground).
- Specimen mechanism: separate claw or combined mechanism to hang specimens.
- Hang: robot hooks onto Submersible bar; passive or active latch.

PROGRAMMING NOTES:
- FTC SDK (Java or Blocks); Linear OpMode common for auto, iterative for teleop.
- Road Runner or Pedro Pathing for auto trajectories.
- Vision: TensorFlow / EasyOpenCV for sample detection; AprilTags for localization.
""",
    },
    "2023": {
        "name": "CenterStage",
        "year": 2023,
        "type": "FTC",
        "context": """
FTC 2023-24 CENTERSTAGE — Season Overview
==========================================
Game: CenterStage (theater/backstage theme)
Field: 12x12 ft, two alliances of 2 robots each.

SCORING ELEMENTS:
- Pixels: flat hexagonal tiles in white/yellow/green/purple.

KEY FIELD ELEMENTS:
- Backdrop: vertical pegboard on alliance wall; pixels placed for points + mosaics.
- Pixel Stack: pre-stacked pixels on field floor.
- Rigging: overhead truss; robots can hang or launch drones in endgame.
- Drone: paper airplane launched by robot in endgame.

MATCH PHASES:
- Auto (30s): Park, spike mark randomization (purple pixel placed), backdrop scoring for bonus.
- Teleop: place pixels on backdrop; build mosaics (3 matching = bonus) and set lines.
- Endgame: Hang on rigging (15pts), park backstage (5pts), launch drone (zones = 30/20/10pts).

COMMON MECHANISMS:
- Pixel intake: passive or active intake from floor stacks.
- Outtake/lift: elevator with claw or arm to place pixels on backdrop at height.
- Hang: robot suspends from rigging bar.

PROGRAMMING NOTES:
- FTC SDK (Java); Road Runner 1.0 widely used for auto.
- Camera + AprilTag detection for auto backdrop alignment.
- Team Prop detection (custom model or color detection) for spike mark randomization.
""",
    },
}

ALL_SEASONS = {**{f"FRC-{k}": v for k, v in FRC_SEASONS.items()}, **{f"FTC-{k}": v for k, v in FTC_SEASONS.items()}}


def get_season_list():
    return [
        {"id": key, "name": f"{val['type']} {val['year']} — {val['name']}", "type": val["type"], "year": val["year"]}
        for key, val in ALL_SEASONS.items()
    ]


def get_system_prompt(season_id: str) -> str:
    season = ALL_SEASONS.get(season_id)
    if not season:
        base_context = "No specific season selected."
    else:
        base_context = season["context"]

    return f"""You are an expert FIRST Robotics assistant specializing in both FRC (FIRST Robotics Competition) and FTC (FIRST Tech Challenge). You help students, mentors, and teams with:
- Robot design and mechanism selection
- Programming strategies and code patterns
- Game strategy and scoring optimization
- Rules clarification and interpretation
- Scouting and data analysis

{f"CURRENT SEASON CONTEXT:{base_context}" if season else ""}

Guidelines:
- Be specific and practical. When discussing mechanisms, mention real-world tradeoffs (weight, complexity, reliability).
- When discussing programming, reference WPILib (FRC) or FTC SDK conventions.
- If asked about statistics or team data, let the user know you can fetch live data from The Blue Alliance (FRC) or FTC Events API when they provide a team number or event code.
- Always clarify FRC vs FTC distinctions when relevant — they have different rules, field sizes, and constraints.
- Keep answers focused and actionable for build season timelines."""
