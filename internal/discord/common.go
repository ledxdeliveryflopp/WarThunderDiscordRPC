package discord

import "time"

var VehicleAirDict = map[string]map[string]string{
	"f_16c_block_50": {"ru": "F-16C Block 50", "en": "F-16C Block 50"},
	"f_15c_msip2":    {"ru": "F-15C \"MSIP II\"", "en": "F-15C \"MSIP II\""},
	"mig_23ml":       {"ru": "МиГ-23МЛ", "en": "MiG-23ML"},
	"mig_29smt_9_19": {"ru": "МиГ-29СМТ (9-19)", "en": "MiG-29SMT (9-19)"},
}

var VehicleGroundDict = map[string]map[string]string{
	"jp_type_90b_camo":           {"ru": "Type 90 (B) \"Fuji\"", "en": "Type 90 (B) \"Fuji\""},
	"germ_leopard_2a4m_can":      {"ru": "Leopard 2A4M CAN", "en": "Leopard 2A4M CAN"},
	"germ_leopard_2a7v":          {"ru": "Leopard 2A7V", "en": "Leopard 2A7V"},
	"germ_leopard_2a5_pso":       {"ru": "Leopard 2 PSO", "en": "Leopard 2 PSO"},
	"us_m1128_wolfpack":          {"ru": "M1128 Wolfpack", "en": "M1128 Wolfpack"},
	"us_m1a1_hc_usmc":            {"ru": "M1A1 Click-Bait", "en": "M1A1 Click-Bait"},
	"germ_leopard_2a4_pzbtl_123": {"ru": "Leopard 2 (PzBtl 123)", "en": "Leopard 2 (PzBtl 123)"},
	"jp_type_16_mod":             {"ru": "Type 16 (FPS)", "en": "Type 16 (FPS)"},
	"ussr_t_80uk":                {"ru": "Т-80УК", "en": "Т-80UK"},
	"germ_leopard_2pl":           {"ru": "Leopard 2 PL", "en": "Leopard 2 PL"},
}

var BasicStateDict = map[string]map[string]string{
	"loading": {"ru": "Загружается в игру", "en": "Loading"},
	"hangar":  {"ru": "В ангаре", "en": "In the hangar"},
}

var StatesDict = map[string]map[string]string{
	"speed_tas":    {"ru": "Скорость TAS", "en": "Speed Tas"},
	"speed_ground": {"ru": "Скорость", "en": "Speed"},
	"crew_count":   {"ru": "Экипаж", "en": "Crew"},
	"altitude":     {"ru": "Высота", "en": "Altitude"},
	"play_on":      {"ru": "Играет на", "en": "Plays on"},
}

var GameTime = time.Now()
