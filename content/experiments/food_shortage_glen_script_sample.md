# サンプル台本 — food_shortage_glen（npc_0042 の記録）

`packaging/script_builder.py` が生成した実出力。各行に由来イベントID（provenance）が付く。

捏造ではなく記録に基づく（§21）。`hedged=True` は断定を避けた解釈行。

| # | Section | Text | Source event_ids | Hedged |
|---|---|---|---|---|
| 1 | Hook | 7日目、戦闘になった。 | evt_0000011 |  |
| 2 | Question | 食料を失った村で、ひとりの農民はどう変わるのか | — |  |
| 3 | Setup | 舞台はglen_village。記録は3日目から始まります。 | evt_0000004 |  |
| 4 | Escalation | 4日目、捕らえられた。ログ上では直前に別の出来事が影響したと記録されています。 | evt_0000005, evt_0000004 | yes |
| 5 | Escalation | 5日目、村を追放された。ログ上では直前に別の出来事が影響したと記録されています。 | evt_0000006, evt_0000005 | yes |
| 6 | Escalation | 6日目、盗賊になった。ログ上では直前に別の出来事が影響したと記録されています。 | evt_0000008, evt_0000006, evt_0000007 | yes |
| 7 | Turning Point | 7日目、戦闘になった。ここが転機でした。 | evt_0000011 |  |
| 8 | Result | 7日目時点の記録では、戦闘になった。 | evt_0000011 |  |
| 9 | Interpretation | npc_0042に何が起きたのか。断定はできませんが、一連の記録からはひとつの因果が読み取れます。 | evt_0000004, evt_0000005, evt_0000006, evt_0000008, evt_0000011 | yes |
| 10 | Steam CTA | GEKOKUJO: Vagrant Crown の世界はSteamで。https://store.steampowered.com/app/4891620/GEKOKUJO_Vagrant_Crown/ | — |  |
