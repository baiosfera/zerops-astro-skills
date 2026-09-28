# HebCal Canonical Reference Pointer

HebCal is maintained as a sovereign first-class Dual-RAG System Skill in the workspace.

## Primary Documentation Links

- **Main Router**: [.agents/skills/hebcal/SKILL.md](file:///var/www/.agents/skills/hebcal/SKILL.md)
- **Comprehensive Usage Manual**: [.agents/skills/hebcal/references/usage.md](file:///var/www/.agents/skills/hebcal/references/usage.md)
- **Infrastructure & Environment Guide**: [.agents/skills/hebcal/references/infra.md](file:///var/www/.agents/skills/hebcal/references/infra.md)

## Integrated Modules Summary

1. **Date Converter & Parashat HaShavua (`/converter`)**: Bidirectional conversion between Gregorian and Hebrew calendars with weekly Torah reading.
2. **Daily Zmanim REST Engine (`/zmanim`)**: Complete daily halachic timestamps (Alot, HaNetz, Shema Gr"a/MGA, Tefila, Chatzot, Mincha, Shkiya, Tzeit).
3. **Shabbat & Havdalah Engine (`/shabbat`)**: Candle lighting, Havdalah, weekly Parasha with aliyot and Haftarah reading.
4. **Jewish Holidays & Fast Days (`/hebcal`)**: Full annual cycle of major/minor holidays, Rosh Chodesh, and fast days.
5. **Sefirat HaOmer & Kabbalistic Sefirot (`/omer`)**: Day-by-day Omer count (1–49) with paired Sefirot combinations (Chesed, Gevurah, Tiferet).
6. **Daily Study Schedules (`/yomi`)**: Talmud Bavli Daf Yomi, Mishneh Torah Rambam, Mishna Yomi, and Nach Yomi.
7. **Multi-Day Zmanim Ranges (`/zmanim?start=...&end=...`)**: Batch date range calculations.
8. **Global Geocoding & Elevation**: Automatic coordinates and timezone resolution with elevation correction.
