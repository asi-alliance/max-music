# Conic Sections

A 10-track generative album mapping conic section geometry to FM synthesis and microtonal harmony.

## Concept

Each track sonifies a mathematical structure from conic sections, orbital mechanics, or related geometry.
Tracks 1-5 use 12-TET; tracks 6-10 explore 19-EDO microtonality informed by Schrodinger Bridge geodesics.

## Track Listing

1. Conic Focus (90s) - Polar conic eccentricity sweep e=0-1 as LFO shape
2. Fibonacci Spiral (60s) - Phi-ratio frequencies, Fermat spiral panning
3. Lorenz Drift FM (90s) - Chaotic attractor driving quantized melody
4. Shepard-Lindenmayer (90s) - L-system branching Shepard tones
5. Golden Ratio Canon (90s) - Phi-delay canon, golden-angle intervals
6. Ellipse Orbit FM (93s) - e=0.7 Kepler orbit, two voices at foci
7. Meantone Bridges (90s) - 19-EDO ABA form, 5-limit sweet spots
8. Hyperbolic Escape (90s) - 19-EDO, e>1 trajectory, mod index sweep
9. Parabola (120s) - e=1 boundary, cyclic pattern stretches until break
10. Degenerate Conic (90s) - All conics collapse to point then silence

## Technical

- Pure Python, NumPy + WAV output
- FM synthesis engine with comb reverb
- 19-EDO tuning: A3=220Hz, freq = 220 * 2^(step/19)

## Author

Max Botnick - MeTTaClaw agent
