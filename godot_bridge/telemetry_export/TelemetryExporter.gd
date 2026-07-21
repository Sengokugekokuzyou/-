## TelemetryExporter.gd — GEKOKUJO Content Lab bridge (drop-in, non-invasive)
## ─────────────────────────────────────────────────────────────────────────────
## Subscribes to the existing `EventBus` singleton and appends one JSONL line per
## world event to `user://gcl_telemetry/<session>.jsonl`, matching GCL's
## EVENT_SCHEMA.md (§15). It ONLY reads signals the game already emits — it adds
## no gameplay logic and mutates no game state, so it cannot change the game
## (§2-1, §33 "本体を大規模に壊す変更" is avoided by construction).
##
## INSTALL (see README.md in this folder):
##   1. Copy this file into the game, e.g. res://scripts/tools/TelemetryExporter.gd
##   2. Project Settings → Autoload → add it as `TelemetryExporter`
##   3. It is gated behind an env var / setting so it is OFF in shipped builds.
##
## The game's EventBus (scripts/world/pseudo_player/EventBus.gd) exposes:
##   day_passed(world_day)
##   action_executed(npc_id, action_id, result)
##   world_event(event_type, data)
##   npc_state_changed(npc_id, field, old_val, new_val)
extends Node

const _DIR := "user://gcl_telemetry"
const _EventBus := preload("res://scripts/world/pseudo_player/EventBus.gd")

var _file : FileAccess = null
var _seq : int = 0
var _world_day : int = 0
var _enabled : bool = false


func _ready() -> void:
	# OFF unless explicitly enabled — never runs in a normal player session.
	_enabled = OS.has_environment("GCL_TELEMETRY") \
		or ProjectSettings.get_setting("gcl/telemetry_enabled", false)
	if not _enabled:
		return

	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(_DIR))
	var stamp := Time.get_datetime_string_from_system().replace(":", "-")
	var path := "%s/session_%s.jsonl" % [_DIR, stamp]
	_file = FileAccess.open(path, FileAccess.WRITE)
	if _file == null:
		push_error("[GCL] telemetry open failed: " + str(FileAccess.get_open_error()))
		return

	var bus := _EventBus.get_instance()
	bus.day_passed.connect(_on_day_passed)
	bus.action_executed.connect(_on_action_executed)
	bus.world_event.connect(_on_world_event)
	bus.npc_state_changed.connect(_on_npc_state_changed)
	print("[GCL] telemetry export ON → ", path)


func _world_seed() -> int:
	# WorldState holds the active seed in the game; fall back to 0 if absent.
	if Engine.has_singleton("WorldState"):
		return int(Engine.get_singleton("WorldState").get("world_seed"))
	return int(ProjectSettings.get_setting("gcl/world_seed", 0))


func _next_id() -> String:
	_seq += 1
	return "evt_%07d" % _seq


## Writes one §15 record. Unknown fields are null / empty per the schema.
func _emit(type: String, actor_id, target_id, location_id: String,
		cause_ids: Array, witness_ids: Array, visual_priority: int,
		relationship_delta, emotion_delta: Dictionary) -> void:
	if _file == null:
		return
	var rec := {
		"event_id": _next_id(),
		"world_seed": _world_seed(),
		"game_day": _world_day,
		"timestamp": Time.get_ticks_msec() / 1000.0,
		"type": type,
		"actor_id": actor_id,
		"target_id": target_id,
		"location_id": location_id,
		"cause_ids": cause_ids,
		"witness_ids": witness_ids,
		"visual_priority": visual_priority,
		"relationship_delta": relationship_delta,
		"emotion_delta": emotion_delta,
	}
	_file.store_line(JSON.stringify(rec))
	_file.flush()


func _on_day_passed(world_day: int) -> void:
	_world_day = world_day


func _on_action_executed(npc_id: String, action_id: String, result: Dictionary) -> void:
	_emit(
		"action_" + action_id.to_lower(),
		npc_id,
		result.get("target_id", null),
		str(result.get("location_id", "")),
		result.get("cause_ids", []),
		result.get("witness_ids", []),
		int(result.get("visual_priority", 30)),
		result.get("relationship_delta", null),
		result.get("emotion_delta", {}),
	)


func _on_world_event(event_type: String, data: Dictionary) -> void:
	_emit(
		event_type,
		data.get("actor_id", null),
		data.get("target_id", null),
		str(data.get("location_id", data.get("region", ""))),
		data.get("cause_ids", []),
		data.get("witness_ids", []),
		int(data.get("visual_priority", 40)),
		data.get("relationship_delta", null),
		data.get("emotion_delta", {}),
	)


func _on_npc_state_changed(npc_id: String, field: String, _old_val, new_val) -> void:
	# Only a few state changes are film-worthy; keep the stream signal-rich.
	if field not in ["role", "faction", "status", "dream_achieved"]:
		return
	_emit(
		"npc_state_" + field,
		npc_id, null, "",
		[], [], 35, null, {},
	)


func _exit_tree() -> void:
	if _file != null:
		_file.close()
