package discord

import "time"

var VehicleAirDict = map[string]map[string]string{
	"f_16c_block_50": {"ru": "F-16C Block 50", "en": "F-16C Block 50"},
	"f_15c_msip2":    {"ru": "F-15C \"MSIP II\"", "en": "F-15C \"MSIP II\""},
	"mig_23ml":       {"ru": "МиГ-23МЛ", "en": "MiG-23ML"},
	"mig_29smt_9_19": {"ru": "МиГ-29СМТ (9-19)", "en": "MiG-29SMT (9-19)"},
	"su_25tm":        {"ru": "Су-39", "en": "Su-39"},
	"mi_24p":         {"ru": "Ми-24П", "en": "Mi-24P"},
	"mi_24v":         {"ru": "Ми-24В", "en": "Mi-24V"},
	"mi_24a":         {"ru": "Ми-24А", "en": "Mi-24A"},
	"mi_4av":         {"ru": "Ми-4АВ", "en": "Mi-4AV"},
	"ah_64d_japan":   {"ru": "AH-64DJP", "en": "AH-64DJP"},
	"ah_1s_late":     {"ru": "AH-1S", "en": "AH-1S"},
	"ah_1s_early":    {"ru": "AH-1E", "en": "AH-1E"},
	"su_33":          {"ru": "Су-33", "en": "Su-33"},
	"ka_50":          {"ru": "Ка-50", "en": "Ka-50"},
}

var VehicleGroundDict = map[string]map[string]string{
	"jp_type_90b_camo":              {"ru": "Type 90 (B) \"Fuji\"", "en": "Type 90 (B) \"Fuji\""},
	"germ_leopard_2a4m_can":         {"ru": "Leopard 2A4M CAN", "en": "Leopard 2A4M CAN"},
	"germ_leopard_2a7v":             {"ru": "Leopard 2A7V", "en": "Leopard 2A7V"},
	"germ_leopard_2a5_pso":          {"ru": "Leopard 2 PSO", "en": "Leopard 2 PSO"},
	"us_m1128_wolfpack":             {"ru": "M1128 Wolfpack", "en": "M1128 Wolfpack"},
	"us_m1a1_hc_usmc":               {"ru": "M1A1 Click-Bait", "en": "M1A1 Click-Bait"},
	"germ_leopard_2a4_pzbtl_123":    {"ru": "Leopard 2 (PzBtl 123)", "en": "Leopard 2 (PzBtl 123)"},
	"jp_type_16_mod":                {"ru": "Type 16 (FPS)", "en": "Type 16 (FPS)"},
	"ussr_t_80uk":                   {"ru": "Т-80УК", "en": "Т-80UK"},
	"germ_leopard_2pl":              {"ru": "Leopard 2 PL", "en": "Leopard 2 PL"},
	"ussr_zprk_2s6":                 {"ru": "2С6 \"Тунгуска\"", "en": "2С6 \"Tunguska\""},
	"ussr_9a35_m2":                  {"ru": "9А35 \"Стрела-10\"", "en": "Strela-10M2"},
	"ussr_t_80bvm":                  {"ru": "Т-80БВМ", "en": "T-80BVM"},
	"ussr_bmp_2m":                   {"ru": "БМП-2М \"Бережок\"", "en": "BMP-2M"},
	"ussr_2s25m":                    {"ru": "2С25М \"Спрут-СДМ1\"", "en": "2S25M"},
	"ussr_t_80u":                    {"ru": "Т-80У", "en": "T-80U"},
	"ussr_2s38":                     {"ru": "2С38 \"Деривация-ПВО\"", "en": "2S38"},
	"ussr_9a33bm3":                  {"ru": "Оса-АКМ (9К33М3)", "en": "Osa-AKM"},
	"ussr_zsu_23_4m4":               {"ru": "ЗСУ-23-4 \"Шилка\"", "en": "ZSU-23-4M4"},
	"ussr_bmp_3":                    {"ru": "БМП-3", "en": "BMP-3"},
	"ussr_object_685":               {"ru": "Объект 685", "en": "Object 685"},
	"ussr_t_10m":                    {"ru": "Т-10М", "en": "T-10M"},
	"ussr_object_435":               {"ru": "Объект 435", "en": "Object 435"},
	"ussr_t_64a_1971":               {"ru": "Т-64А (1971)", "en": "T-64A (1971)"},
	"ussr_t_64_b_1984":              {"ru": "Т-64Б", "en": "Т-64Б"},
	"ussr_t_55a":                    {"ru": "Т-55", "en": "T-55"},
	"germ_schutzenpanzer_puma_vjtf": {"ru": "PUMA VJTF", "en": "PUMA VJTF"},
	"germ_leopard_2a6":              {"ru": "Leopard 2A6", "en": "Leopard 2A6"},
	"germ_leopard_2a4":              {"ru": "Leopard 2A4", "en": "Leopard 2A4"},
	"germ_leopard_2k":               {"ru": "Leopard 2K", "en": "Leopard 2K"},
	"germ_radpanzer_90":             {"ru": "Radkampfwagen 90", "en": "Radkampfwagen 90"},
	"germ_begleitpanzer_57":         {"ru": "Begleitpanzer 57", "en": "Begleitpanzer 57"},
	"germ_thyssen_henschel_tam":     {"ru": "ТАМ", "en": "ТАМ"},
	"germ_sk105_a2":                 {"ru": "JaPz.K A2", "en": "JaPz.K A2"},
	"germ_mkpz_m48a2ga2":            {"ru": "M48A2 G A2", "en": "M48A2 G A2"},
	"germ_kpz_70":                   {"ru": "KPz-70", "en": "KPz-70"},
	"germ_mkpz_super_m48":           {"ru": "M48 Super", "en": "M48 Super"},
	"germ_kpz_t72m1":                {"ru": "◊T-72M1", "en": "◊T-72M1"},
	"germ_leopard_I_a1":             {"ru": "Leopard A1A1", "en": "Leopard A1A1"},
	"germ_leopard_1a5":              {"ru": "Leopard 1A5", "en": "Leopard 1A5"},
	"germ_leopard_a1a1_120":         {"ru": "Leopard A1A1 (L/44)", "en": "Leopard A1A1 (L/44)"},
	"us_m60a1":                      {"ru": "M60A1 (AOS)", "en": "M60A1 (AOS)"},
	"us_t95e1":                      {"ru": "T95E1", "en": "T95E1"},
	"us_xm_803":                     {"ru": "XM803", "en": "XM803"},
	"us_mbt_70":                     {"ru": "MBT-70", "en": "MBT-70"},
	"us_m247":                       {"ru": "M247", "en": "M247"},
	"us_mim_72_chaparral":           {"ru": "MIM-72 Chaparral", "en": "MIM-72 Chaparral"},
	"us_xm_975_roland":              {"ru": "XM975", "en": "XM975"},
	"us_m1_abrams":                  {"ru": "M1 Abrams", "en": "M1 Abrams"},
	"us_m1a1_aim_abrams":            {"ru": "M1A1 AIM", "en": "M1A1 AIM"},
	"us_m1_abrams_kvt":              {"ru": "M1 KVT", "en": "M1 KVT"},
	"jp_type_81_tansam":             {"ru": "Type 81 (C)", "en": "Type 81 (C)"},
	"jp_type_93":                    {"ru": "Type 93", "en": "Type 93"},
	"jp_type_87":                    {"ru": "Type 87", "en": "Type 87"},
	"jp_type_16_mcv_prot":           {"ru": "Type 16 (P)", "en": "Type 16 (P)"},
	"jp_tkx_prot":                   {"ru": "TKX", "en": "TKX"},
	"jp_type_10":                    {"ru": "Type 10", "en": "Type 10"},
	"jp_type_90b":                   {"ru": "Type 90 (B)", "en": "Type 90 (B)"},
	"jp_type_74_f":                  {"ru": "Type 74 (F)", "en": "Type 74 (F)"},
}

var BasicStateDict = map[string]map[string]string{
	"loading": {"ru": "Загружается в игру", "en": "Loading"},
	"hangar":  {"ru": "В ангаре", "en": "In the hangar"},
}

var VehicleStatesDict = map[string]map[string]string{
	"speed_tas":    {"ru": "Скорость TAS", "en": "Speed Tas"},
	"speed_ground": {"ru": "Скорость", "en": "Speed"},
	"crew_count":   {"ru": "Экипаж", "en": "Crew"},
	"altitude":     {"ru": "Высота", "en": "Altitude"},
	"play_on":      {"ru": "Играет на", "en": "Plays on"},
}

var GameTime = time.Now()
