# USDT Investigator design system

## Direction

A bounded crypto-investigation casebook. The visual language should foreground transaction evidence, uncertainty and analytical limits instead of presenting a flashy blockchain visualization.

## Foundations

- **Typography:** Public Sans for the interface; system monospace for addresses, hashes and exact transfer evidence.
- **Canvas:** deep navy (`#09131f`) with restrained analytical surfaces (`#102131`).
- **Signals:** mint (`#69d3bc`) for selected evidence and primary actions; amber (`#d6a958`) for limitations and caution.
- **Geometry:** thin borders and small control radii. Avoid glow, decorative glyphs, gradients and exaggerated card effects.
- **Spacing:** compact around tools and tables; wider around the case purpose and investigation narrative.

## Components and interaction

- The purpose statement explains the use case and limitations before the graph.
- Graph selection must also update textual evidence; color and position are never the only explanation.
- Transaction hashes, amounts and timestamps remain exact and inspectable.
- Buttons and disclosures are at least 44px high with visible keyboard focus.
- Reduced-motion preferences remove control transitions without disabling core interaction.

## Responsive behavior

The graph and evidence panel stack on narrow screens. Dense transactions remain horizontally scrollable so hashes and amounts are not silently truncated.
