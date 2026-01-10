import os, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

ROADMAP_LINKS = {
    "cse_rm_ai": "رابط مسار AI & Machine learning:\n🔗https://qr1.me-qr.com/mobile/pdf/4a687b37-8557-4f38-92ac-5f621fedd2c1",
    "cse_rm_ds": "رابط مسار علم البيانات (Data Science):\n🔗https://qr1.me-qr.com/mobile/pdf/63e394f8-a86b-4e3e-9455-f2151b4f12b5",
    "cse_rm_robotics": "رابط مسار الروبوتات:\n🔗https://qr1.me-qr.com/mobile/pdf/d1770eda-eaec-47c7-aefe-d6b04597d1d9",
    "cse_rm_cyber": "رابط مسار الأمن السيبراني:\n🔗https://qr1.me-qr.com/mobile/pdf/f4e9fa7c-f7ec-49a4-9243-f47fe7c6fdfd",
    "cse_rm_fullstack": "رابط مسار الفل ستاك(full stack developer):\n🔗https://qr1.me-qr.com/mobile/pdf/a51e8960-56fa-4612-a106-ad53ee7fa2a3",
    "cse_rm_frontend": "رابط مسار الفرونت إند(frontend developer):\n🔗https://qr1.me-qr.com/mobile/pdf/cd5c2ece-0e69-4ddd-b084-a49708d41b42",
    "cse_rm_backend": "رابط مسار الباك إند (backend developer):\n🔗https://qr1.me-qr.com/mobile/pdf/5f99a65a-fc13-4819-bd44-9168c187134b",
    "cse_rm_mobile": "رابط مسار الأندرويد:\n🔗https://qr1.me-qr.com/mobile/pdf/994f5141-2fd1-462a-8892-10d0982ed45b\n\nرابط مسار IOS:\n🔗https://qr1.me-qr.com/mobile/pdf/a53e5055-04e7-401d-ae16-5ee0809503d2",
    "cse_rm_uiux": "رابط مسار تصميم واجهة المستخدم (UI/UX designer):\n🔗https://qr1.me-qr.com/mobile/pdf/3698c9fa-53a8-4284-9ce7-d2052847bc8a",
    "cse_rm_qa": "رابط مسار ضمان الجودة (QA Engineer):\n🔗https://qr1.me-qr.com/mobile/pdf/79c31563-de01-4d08-a618-92cad8d4d535",
    "cse_rm_lowlevel": "رابط مسار اللغات منخفضة المستوى (LL Programming):\n🔗https://qr1.me-qr.com/mobile/pdf/42137ab5-0755-4824-9f23-707f8f2e3df0",
    "cse_rm_game": "رابط مسار تطوير الألعاب (Game Developer):\n🔗https://qr1.me-qr.com/mobile/pdf/3f97d69d-378b-44a2-b8b5-662263da891c",
}

SUBJECT_LINKS = { 

    # هندسة الاتصالات – إجباري تخصص
    "te_dm_mic": "🔗 كل ما يخص مادة متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/15jlZjQKiTjJgMLO28f_h4u79IE5XYisr",
    "te_dm_mcl": "🔗 كل ما يخص مادة مختبر متحكمات دقيقة:\nhttps://drive.google.com/drive/folders/1vdD5m2AxEr5W3QtIWu42SBdPf95wUND_?hl=ar",
    "te_dm_dld": "🔗 كل ما يخص مادة تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI",
    "te_dm_dll": "🔗 كل ما يخص مادة مختبر تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar",
    "te_dm_ele": "🔗 كل ما يخص مادة إلكترونيات:\nhttps://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb",
    "te_dm_lel": "🔗 كل ما يخص مادة مختبر إلكترونيات:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar",
    "te_dm_ctl": "🔗 كل ما يخص مادة أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar",
    "te_dm_lcl": "🔗 كل ما يخص مادة مختبر أنظمة تحكم 1:\nhttps://drive.google.com/drive/folders/1iJuSOKY6c1LQ8oZ15ncKiaVxEOGlCHst?hl=ar",
    "te_dm_ec1": "🔗 كل ما يخص مادة دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1zWr2kk4jznsqB2_VyDwUrlXAomX2ppJy",
    "te_dm_lec": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 1:\nhttps://drive.google.com/drive/folders/1LOn0kXufvISSPDu3X7BiMSY3u5xnppWh?hl=ar",
    "te_dm_ec2": "🔗 كل ما يخص مادة دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/11zw1ss3cgU3fX5xE3pd1bMAthrvUsasa",
    "te_dm_lc2": "🔗 كل ما يخص مادة مختبر دوائر كهربائية 2:\nhttps://drive.google.com/drive/folders/1exrz303ktSkMn26VpbyR-dwwBH0MlEiL?hl=ar",
    "te_dm_dcm": "🔗 كل ما يخص مادة اتصالات رقمية:\nhttps://drive.google.com/drive/folders/1CCcNu0Y_DWD9lNSorrqAMnO6wfsNgWHV",
    "te_dm_prb": "🔗 كل ما يخص مادة الاحتمالات والمتغيرات العشوائية:\nhttps://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV",
    "te_dm_acm": "🔗 كل ما يخص مادة اتصالات تماثلية:\nhttps://drive.google.com/drive/folders/1ZCQDftVAUNN6pufMmFz2MniZkK2OJvTp",
    "te_dm_sig": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "te_dm_emg": "🔗 كل ما يخص مادة كهرومغناطيسية:\nhttps://drive.google.com/drive/folders/11EZrizxPcbYY3xjGseDeOLLdFsIEunvM",
    "te_dm_aec": "🔗 كل ما يخص مادة إلكترونيات متقدمة للاتصالات:\nhttps://drive.google.com/drive/folders/1SOL5I1Im3twNrfKieLj0Kc4TWB30jowj",
    "te_dm_net": "🔗 كل ما يخص مادة شبكات حاسوب:\nhttps://drive.google.com/drive/folders/11xXsav473CKMGf36TZdIOj39StalkIAt",
    "te_dm_prg": "🔗 كل ما يخص مادة برمجة حاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar",
    "te_dm_aew": "🔗 كل ما يخص مادة الصوتيات والأمواج الكهرومغناطيسية:\nhttps://drive.google.com/drive/folders/1v7AWzoyTWJ5CADo-68oNMtp4hbXaCSfC",
    "te_dm_ofs": "🔗 كل ما يخص مادة أنظمة الألياف الضوئية:\nhttps://drive.google.com/drive/folders/13IlmE6sMct-gAdZxoTmhlZJxNJGGBjXN",
    "te_dm_ant": "🔗 كل ما يخص مادة الهوائيات وانتشار الأمواج:\nhttps://drive.google.com/drive/folders/1zRh06odBIGSNOkxwZwa7ONJ5JiAa-KJC",
    "te_dm_spc": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة:\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",
    "te_dm_num": "🔗 كل ما يخص مادة تحليل عددي:\nhttps://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj",

    
    # هندسة الحاسوب – إجباري تخصص
    "cse_dm_cpp": "🔗 كل ما يخص مادة برمجة الحاسوب:\nhttps://drive.google.com/drive/folders/1dfB641lJ4aW7OCMhiXzb9CbHD57ScRKY?hl=ar",
    "cse_dm_dslab": "🔗 كل ما يخص مادة مختبر تركيب البيانات:\nhttps://drive.google.com/drive/folders/1eMTzUX_1TvhkoWctA64IsHP7nokKtTVa?hl=ar",
    "cse_dm_dis": "🔗 كل ما يخص مادة تراكيب الحوسبة المتقطعة:\nhttps://drive.google.com/drive/folders/1r19VoO7Jn3th47Yvv02xqp_j_cRIANer?hl=ar",
    "cse_dm_alg": "🔗 كل ما يخص مادة الخوارزميات:\nhttps://drive.google.com/drive/folders/1HW8jr8rkYG1mCTu5Hw7V9bu6XrlMLj1K?hl=ar",
    "cse_dm_os": "🔗 كل ما يخص مادة نظم التشغيل:\nhttps://drive.google.com/drive/folders/1h5UMPn2E9PKEbApKMgr5gw6fcQD75ICX?hl=ar",
    "cse_dm_db": "🔗 كل ما يخص مادة أنظمة قواعد البيانات:\nhttps://drive.google.com/drive/folders/1As24z-MhrkxUgOQCTvxulg3ZscQL2X01?hl=ar",
    "cse_dm_dblab": "🔗 كل ما يخص مادة مختبر أنظمة قواعد البيانات:\nhttps://drive.google.com/drive/folders/1gC2wrrVNaC2pFtTehECBQTq1YbVJ4fTW?hl=ar",
    "cse_dm_net": "🔗 كل ما يخص مادة شبكات الحاسوب:\nhttps://drive.google.com/drive/folders/1bHhvXwaW1gp1CnDiNqOpK8iuytzc5H31?hl=ar",
    "cse_dm_netlab": "🔗 كل ما يخص مادة مختبر شبكات الحاسوب:\nhttps://drive.google.com/drive/folders/1y1D1FDgygSb0fZihJya49RzePjdp874u?hl=ar",
    "cse_dm_isad": "🔗 كل ما يخص مادة تحليل وتصميم أنظمة المعلومات:\nhttps://drive.google.com/drive/folders/1oLU6aQTdXa7ktuODLajyWRrvO1AowfiZ?hl=ar",
    "cse_dm_arc": "🔗 كل ما يخص مادة معمارية الحاسوب:\nhttps://drive.google.com/drive/folders/1Ykp8VwEvfIgk0cJcLyZf6l8YY71fDftQ?hl=ar",
    "cse_dm_ass": "🔗 كل ما يخص مادة الأسمبلي:\nhttps://drive.google.com/drive/folders/1Mar8liqfh9GtAuJt_3HLhvy1F9df9iuF?hl=ar",
    "cse_dm_asslab": "🔗 كل ما يخص مادة مختبر الأسمبلي:\nhttps://drive.google.com/drive/folders/1Z8lWitiU9XDp5p8-fCKOvRklf4P0y7QT?hl=ar",
    "cse_dm_soft": "🔗 كل ما يخص مادة هندسة البرمجيات:\nhttps://drive.google.com/drive/folders/1I6Qon3_jvBG4KoGtmwQ1qBabzuA1ztvW?hl=ar",
    "cse_dm_netpro": "🔗 كل ما يخص مادة برمجة الشبكات:\nhttps://drive.google.com/drive/folders/1KGn9YDVnoZZVDPjfYa516ToWJHQZJmKm?hl=ar",
    "cse_dm_vhdl": "🔗 كل ما يخص مادة التصميم المنطقي عالي المستوى:\nhttps://drive.google.com/drive/folders/1cQhqZuOg05wOhLBfJCDErHo5Sdh9GWaD?hl=ar",
    "cse_dm_web": "🔗 كل ما يخص مادة تقنيات الانترنت وتطبيقات الويب:\nhttps://drive.google.com/drive/folders/1wz3InGxK3ZkUzeKVgACEB7k_lAP8Fyaa?hl=ar",
    "cse_dm_ai": "🔗 كل ما يخص مادة الذكاء الاصطناعي:\nhttps://drive.google.com/drive/folders/1EGiAnJdtjmYP6q5WxbvOzz4rd0O6nf0I?hl=ar",
    "cse_dm_cir": "🔗 كل ما يخص مادة الدوائر الكهربائية:\nhttps://drive.google.com/drive/folders/1Y4BPIHpd21iBm_9wSfDYPcyLFbBeU_kb",
    "cse_dm_cirlab": "🔗 كل ما يخص مادة مختبر الدوائر الكهربائية:\nhttps://drive.google.com/drive/folders/1oh7bNZxJtEows95EjCNRawxlfZ8SzZ8U?hl=ar",
    "cse_dm_ele": "🔗 كل ما يخص مادة الإلكترونيات:\nhttps://drive.google.com/drive/folders/1yqAMOJf0Ob7Ld5IYDuCKPDWM5kz6s5bb",
    "cse_dm_elelab": "🔗 كل ما يخص مادة مختبر الإلكترونيات:\nhttps://drive.google.com/drive/folders/1RBpecgw5nRWkugynmwB1sueYYIzjgtSn?hl=ar",
    "cse_dm_dig": "🔗 كل ما يخص مادة تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/1-BTgAZ72Kf5C-da2HDNujLNHXduwZPCI",
    "cse_dm_diglab": "🔗 كل ما يخص مادة مختبر تصميم الدوائر المنطقية:\nhttps://drive.google.com/drive/folders/17wxfFU38kZMXB1bm5sWt4n_wArM92jeQ?hl=ar",
    "cse_dm_dige": "🔗 كل ما يخص مادة إلكترونيات رقمية:\nhttps://drive.google.com/drive/folders/10BaqCIeCxxGmZFtNf0iHjLp0PGnXM3xe",
    "cse_dm_sig": "🔗 كل ما يخص مادة الإشارات والنظم:\nhttps://drive.google.com/drive/folders/1SrP1dsUG0rzOQA3cpEc9zZx1FG9kMZd0",
    "cse_dm_pro": "🔗 كل ما يخص مادة الاحتمالات والمتغيرات العشوائية:\nhttps://drive.google.com/drive/folders/1gahG9TeHuRpCmjHdUvLMnxktIxMDIcmV",
    "cse_dm_cs": "🔗 كل ما يخص مادة أنظمة الاتصالات:\nhttps://drive.google.com/drive/folders/12ZENHtxlaqjpYgV79NTBgDiNBqIqcfsn",
    "cse_dm_dsp": "🔗 كل ما يخص مادة معالجة الإشارات الرقمية:\nhttps://drive.google.com/drive/folders/1uXoNhnC_6O_Z-0EdQxZ4YUXNd1q74YUd",
    "cse_dm_con": "🔗 كل ما يخص مادة كنترول 1:\nhttps://drive.google.com/drive/folders/1LKP0BRQ019aOhT1Mu9AYZCxWa1wxMk7F?hl=ar",
    "cse_dm_num": "🔗 كل ما يخص مادة تحليل عددي:\nhttps://drive.google.com/drive/folders/1w59DQ7uRTLqCrKpJUE4-CLxTSsrESBOj",

    # هندسة الاتصالات – اختياري تخصص
    "te_do_web": "🔗 كل ما يخص مادة تقنيات الانترنت وتطبيقات الويب:\nhttps://drive.google.com/drive/folders/1wz3InGxK3ZkUzeKVgACEB7k_lAP8Fyaa?hl=ar",
    "te_do_oop": "🔗 كل ما يخص مادة البرمجة الكينونية:\nhttps://drive.google.com/drive/folders/16mlcz7332pqsXWDcVM45Ez9Hi8KE2DWN?hl=ar",
    "te_do_db": "🔗 كل ما يخص مادة تركيب البيانات:\nhttps://drive.google.com/drive/folders/1MU9nY5LtI6_qzvvlIsM8p_JE9-OgYi7Z?hl=ar",
    "te_do_swe": "🔗 كل ما يخص مادة هندسة البرمجيات:\nhttps://drive.google.com/drive/folders/1I6Qon3_jvBG4KoGtmwQ1qBabzuA1ztvW?hl=ar",
    "te_do_cod": "🔗 كل ما يخص مادة نظرية المعلومات والترميز (كودينج):\nhttps://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4",
    
    # هندسة الحاسوب – اختياري تخصص
    "cse_do_adb": "🔗 كل ما يخص مادة مواضيع متقدمة في قواعد البيانات:\nhttps://drive.google.com/drive/folders/1yz8LMm1E4ErufxXHsA2ZBXw29cThH8wN?usp=drive_link",
    "cse_do_fib": "🔗 كل ما يخص مادة أنظمة الألياف الضوئية:\nhttps://drive.google.com/drive/folders/13IlmE6sMct-gAdZxoTmhlZJxNJGGBjXN",
    "cse_do_cs": "🔗 كل ما يخص مادة التشفير وأمن الشبكات:\nhttps://drive.google.com/drive/folders/11QMuiAHOtzktbKzEdXJkfpxf6h84neqt?hl=ar",
    "cse_do_acse": "🔗 كل ما يخص مادة مواضيع خاصة في هندسة أنظمة الحاسوب:\nhttps://drive.google.com/drive/folders/1yz8LMm1E4ErufxXHsA2ZBXw29cThH8wN?usp=drive_link",
    "cse_do_ml": "🔗 كل ما يخص مادة تعلم الآلة:\nhttps://drive.google.com/drive/folders/1r9W75-GeMHrNeNT7KXF-r_zqBM7QyoLp?hl=ar",
    "cse_do_dis": "🔗 كل ما يخص مادة أنماط التصميم:\nhttps://drive.google.com/drive/folders/1-KqrAUZeX7QYF4hHUqaDMnVMqLpFbx2k?hl=ar",
    "cse_do_dm": "🔗 كل ما يخص مادة تنجيم البيانات:\nhttps://drive.google.com/drive/folders/1yRaeasZdEedjtbgvAC2gY2c1JggQeAyL?hl=ar",
    "cse_do_cod": "🔗 كل ما يخص مادة نظرية المعلومات والترميز (كودينج):\nhttps://drive.google.com/drive/folders/1DPEIqsLX9Cq3kwE7I8wdk43oCT1tzvO4",
    "cse_do_sen": "🔗 كل ما يخص مادة المجسات ومحولات الطاقة (سنسور):\nhttps://drive.google.com/drive/folders/1SEwhdFIG4jV-uISW0IB7BzgKjScHogwm",

    # إجباري الجامعة
    "shared_um_pi": "🔗 كل ما يخص مادة القضية الفلسطينية:\nhttps://drive.google.com/drive/folders/1AsOgF_Dqp2LKbKnfNjw12fTcEsx8-DI0",
    "shared_um_ar": "🔗 كل ما يخص مادة اللغة العربية:\nhttps://drive.google.com/drive/folders/16wiqvllo8uDoOt3mYA_tB_L8_DHmNG4F",
    "shared_um_cs": "🔗 كل ما يخص مادة مهارات الحاسوب:\nhttps://drive.google.com/drive/folders/1AqY3HGTmsEKJR-hUXoqR5-EeT-HE0HUe",
    "shared_um_com": "🔗 كل ما يخص مادة مهارات الاتصال:\nhttps://drive.google.com/drive/folders/1ag6esdUXaaFg8hKQRtdtTqjMIsPPLqxh",
    "shared_um_en": "🔗 كل ما يخص مادة اللغة الإنجليزية 1:\nhttps://drive.google.com/drive/folders/1QbSzV5flY50kuT1IrtFu-DhwZ4fc0dv7",
    "shared_um_is": "🔗 كل ما يخص مادة الدراسات الإسلامية:\nhttps://drive.google.com/drive/folders/1l_p-WrNOhr21VDdDE7FpNLy3QAbn1qg0",
    "shared_um_men": "🔗 كل ما يخص مادة استدراكي اللغة الإنجليزية:\nhttps://drive.google.com/drive/folders/1zoPLhWLfna2YHdZSQ5W2zMU9dDiiLq4I",

    # إجباري الكلية
    "shared_cm_chy1": "🔗 كل ما يخص مادة كيمياء عامة 1:\nhttps://drive.google.com/drive/folders/1_iO_Yk82kHH0bPz5I06lz1a8-2bt5o8N",
    "shared_cm_lin1": "🔗 كل ما يخص مادة رياضيات هندسية 1:\nhttps://drive.google.com/drive/folders/1p1uokT1-inoyoloh-AhYZ5GBmYiz1_UU",
    "shared_cm_lin2": "🔗 كل ما يخص مادة رياضيات هندسية 2:\nhttps://drive.google.com/drive/folders/16OqtFroWpAV0QgyVEIiIwrU0ICuoGoaj",
    "shared_cm_phy1": "🔗 كل ما يخص مادة فيزياء عامة 1:\nhttps://drive.google.com/drive/folders/1eTrvltnuqp8AHNQUS7JWffjC2ei9LAMM",
    "shared_cm_phy2": "🔗 كل ما يخص مادة فيزياء عامة 2:\nhttps://drive.google.com/drive/folders/1al3U6btk6IMrhDS-zC-uOYHkaF2YgkZ9",
    "shared_cm_cal1": "🔗 كل ما يخص مادة تفاضل وتكامل 1:\nhttps://drive.google.com/drive/folders/1FJFRsOX9isi5FpqIt3UhsceQZfxmZcQS",
    "shared_cm_cal2": "🔗 كل ما يخص مادة تفاضل وتكامل 2:\nhttps://drive.google.com/drive/folders/1JpqO5Pa7P0xk0D6C1auVNDCy_yqFnmgl",
    "shared_cm_phyl1": "🔗 كل ما يخص مادة مختبر فيزياء عامة 1:\nhttps://drive.google.com/drive/folders/1h_aqGgyD5V-IpG91KgUvCPec89FeSVtP?hl=ar",
    "shared_cm_phyl2": "🔗 كل ما يخص مادة مختبر فيزياء عامة 2:\nhttps://drive.google.com/drive/folders/1nO-MDLUo7-ihBxq-l-t2WG9au9ejWqWM?hl=ar",
    "shared_cm_ee": "🔗 كل ما يخص مادة اقتصاد هندسي:\nhttps://drive.google.com/drive/folders/1LiWsRZMwQH1LlKF513cy-umELAgankIO",
    "shared_cm_el": "🔗 كل ما يخص مادة مشغل هندسي:\nhttps://drive.google.com/drive/folders/1xYwCFikleDJloKnOG1jV5xtz4NSBMunG?hl=ar",
    "shared_cm_ed": "🔗 كل ما يخص مادة رسم هندسي:\nhttps://drive.google.com/drive/folders/19yDHfznncH4DuqWh5SlCy2siAZpNm7PV?hl=ar",
    "shared_cm_en2": "🔗 كل ما يخص مادة اللغة الإنجليزية 2:\nhttps://drive.google.com/drive/folders/1byU064ptdQ1mAxMSA8-twk8F5QZIp7Sy",
    "shared_cm_tw": "🔗 كل ما يخص مادة الكتابة التقنية وأخلاقيات المهنة:\nhttps://drive.google.com/drive/folders/1AjAp3qXHr4jEpCIuSlJktcAyX4pyPOK6?hl=ar",
    "shared_cm_sr": "🔗 كل ما يخص مادة مقدمة في منهجية البحث العلمي:\nhttps://drive.google.com/drive/folders/1ACRINqfCFGBZpLQGHtWUWyF5bVbC3Wj0?hl=ar",

    # اختياري الجامعة
    "shared_uo_spo": "🔗 كل ما يخص مادة الريادة والإبداع:\nhttps://drive.google.com/drive/folders/1BSYpLtfklUmW1UoimwokK-MZwGl99h4B",
    "shared_uo_aid": "🔗 كل ما يخص مادة إسعافات أولية:\nhttps://drive.google.com/drive/folders/1eMYmt_RpY6K-8xozQ83C3qtfc_iGLsLj",
    "shared_uo_hel": "🔗 كل ما يخص مادة الرياضة والصحة:\nhttps://drive.google.com/drive/folders/1_epsNMs45Pdqvk0AdWMaWLYtd0zZ9M5K",
    "shared_uo_isl": "🔗 كل ما يخص مادة الفكر الإسلامي:\nhttps://drive.google.com/drive/folders/1tfqMI736xu9bFpete1wxmNVE1jr1tTl7",
    "shared_uo_law": "🔗 كل ما يخص مادة القانون في حياتنا:\nhttps://drive.google.com/drive/folders/1_syfDYEHmtduIWok1u_jnkFBQ6WbqjV_",
    "shared_uo_chi": "🔗 كل ما يخص مادة تنشئة الأطفال:\nhttps://drive.google.com/drive/folders/1uQKcXDGt03A3Y_1c63nd7IUhfNZgUe0U",
    "shared_uo_civ": "🔗 كل ما يخص مادة حضارة إسلامية:\nhttps://drive.google.com/drive/folders/1z3q-13a_rOFO6dtZbMjAGwNEwCh2P1KV",
    "shared_uo_asp": "🔗 كل ما يخص مادة حركة أسيرة:\nhttps://drive.google.com/drive/folders/1-80OIWdDTtaapkyiURGmFpR4jLDg-UK_",
    "shared_uo_car": "🔗 كل ما يخص مادة مقدمة في هندسة السيارات:\nhttps://drive.google.com/drive/folders/1M6Ovliw7EJ9awE6Kg9oJuK4fG-EDTt5j",
    "shared_uo_iss": "🔗 كل ما يخص مادة قضايا معاصرة:\nhttps://drive.google.com/drive/folders/1-9b_H2IMbZLU3mg_aw1MpicFsCZsR6vw",
    "shared_uo_ant": "🔗 كل ما يخص مادة مكافحة الفساد:\nhttps://drive.google.com/drive/folders/1O-chfPMtuD-s2LBH9GW-H-x-qIYh6jBZ",
    "shared_uo_tur": "🔗 كل ما يخص مادة اللغة التركية:\nhttps://drive.google.com/drive/folders/1SgqSxvQruuFVIdOoYOw2tcDF3upC0jGC?hl=ar",
    "shared_uo_lib": "🔗 كل ما يخص مادة المكتبة وطرق البحث:\nhttps://drive.google.com/drive/folders/1X4AvmeV5CcQXvXmcsBqdmuiu_OK5WXOR",
    "shared_uo_heb": "🔗 كل ما يخص مادة اللغة العبرية:\nhttps://drive.google.com/drive/folders/1FuWbM2ZHMSsf4Gnp1TxeVA9mTzeoAZ5Q?hl=ar",
    "shared_uo_com": "🔗 كل ما يخص مادة مهارات التواصل المهني:\nhttps://drive.google.com/drive/folders/1ihs9BylIKUSQBIoRSWHxI18XTF2bbrmM?hl=ar",
    "shared_uo_jer": "🔗 كل ما يخص مادة تاريخ القدس:\nhttps://drive.google.com/drive/folders/1NMuX-KEWdye6nuYRTjb-qZk2aYwH0kwH?hl=ar",
}

# =========================
# Helpers
# =========================

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💻 هندسة الحاسوب", callback_data="cse"), InlineKeyboardButton("📡 هندسة الاتصالات", callback_data="te")],
        [InlineKeyboardButton("⚙️ هندسة الميكانيك", callback_data="me"), InlineKeyboardButton("⚙️ هندسة الميكاترونيكس", callback_data="me")],
        [InlineKeyboardButton("⚡ الهندسة الكهربائية والأتمتة الصناعية", callback_data="ee")],
        [InlineKeyboardButton("🏗 هندسة البناء", callback_data="ce"), InlineKeyboardButton("🏗 الهندسة المدنية", callback_data="ce")],
        [InlineKeyboardButton("📚 مواد مشتركة", callback_data="shared_subjects")],
        [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")]
    ])


def specialization_menu(spec_code: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 إجباري تخصص", callback_data=f"{spec_code}_dm"), InlineKeyboardButton("📗 اختياري تخصص", callback_data=f"{spec_code}_do")],
        [InlineKeyboardButton("📚 مواد مشتركة", callback_data="shared_subjects")],
        [InlineKeyboardButton("Roadmaps", callback_data=f"{spec_code}_roadmaps"), InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ])



# def subjects_menu(spec_code: str):
#     return InlineKeyboardMarkup([
#         [InlineKeyboardButton("🔙 رجوع", callback_data=spec_code), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
#     ])

def shared_subjects_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 إجباري الجامعة", callback_data="shared_um")],
        [InlineKeyboardButton("📗 إجباري الكلية", callback_data="shared_cm")],
        [InlineKeyboardButton("📙 اختياري الجامعة", callback_data="shared_uo")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ])

# =========================
# Commands
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "👋 أهلاً بك في بوت الهندسة الجامعية\n\n"
        "📌 **طريقة استخدام البوت:**\n"
        "• البوت يعمل بالكامل عبر الأزرار.\n"
        "• اختر تخصصك من القائمة الرئيسية.\n"
        "• ادخل إلى قسم المواد ثم اختر نوع المادة.\n"
        "• داخل كل مادة ستجد التلاخيص، الشروحات، الكتب، الامتحانات وغيرها.\n"
        "• يمكنك دائمًا الرجوع باستخدام زر (رجوع).\n\n"
        "💡 لأي ملاحظات أو اقتراحات استخدم الأمر:\n"
        "/note\n\n"
        "👇 اختر من القائمة:"
    )

    await update.message.reply_text(
        intro_text,
        reply_markup=main_menu_keyboard()
    )


async def inst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 هذا البوت تعليمي يعتمد على القوائم.\n"
        "تنقّل بين التخصصات والمواد باستخدام الأزرار فقط."
    )


# async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "🤖 البوتات المرتبطة:\n"
#         "@tamfk2006\n"
#         "@Tak6Bot\n"
#         "@IVR_Library_bot"
#     )


# =========================
# Callback Buttons
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ---- Main specializations ----
    
    if data == "shared_subjects":
        await query.edit_message_text(
            text="📚 المواد المشتركة بين جميع التخصصات:",
            reply_markup=shared_subjects_menu()
        )

    elif data =="shared_um":
        await query.edit_message_text(
            text="📚 إجباري الجامعة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("مهارات الحاسوب", callback_data=f"{data}_cs"), InlineKeyboardButton("مهارات الاتصال", callback_data=f"{data}_com")],
                [InlineKeyboardButton("اللغة العربية", callback_data=f"{data}_ar"), InlineKeyboardButton("اللغة الإنجليزية 1", callback_data=f"{data}_en")],
                [InlineKeyboardButton("الدراسات الإسلامية", callback_data=f"{data}_is"), InlineKeyboardButton("القضية الفلسطينية", callback_data=f"{data}_pi")],
                [InlineKeyboardButton("استدراكي اللغة الإنجليزية", callback_data=f"{data}_men")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data=="shared_cm":
        await query.edit_message_text(
            text="📚 إجباري الكلية:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رسم هندسي", callback_data=f"{data}_ed"),InlineKeyboardButton("مشغل هندسي", callback_data=f"{data}_el"), InlineKeyboardButton("اقتصاد هندسي", callback_data=f"{data}_ee")],
                [InlineKeyboardButton("الكتابة التقنية وأخلاقيات المهنة", callback_data=f"{data}_tw")],
                [InlineKeyboardButton("تفاضل وتكامل 1", callback_data=f"{data}_cal1"),InlineKeyboardButton("تفاضل وتكامل 2", callback_data=f"{data}_cal2")],
                [InlineKeyboardButton("رياضيات هندسية 1", callback_data=f"{data}_lin1"),InlineKeyboardButton("رياضيات هندسية 2", callback_data=f"{data}_lin2")],
                [InlineKeyboardButton("فيزياء عامة 1", callback_data=f"{data}_phy1"),InlineKeyboardButton("فيزياء عامة 2", callback_data=f"{data}_phy2")],
                [InlineKeyboardButton("مختبر فيزياء 1", callback_data=f"{data}_phyl1"),InlineKeyboardButton("مختبر فيزياء 2", callback_data=f"{data}_phyl2")],
                [InlineKeyboardButton("كيمياء عامة 1", callback_data=f"{data}_chy1"),InlineKeyboardButton("اللغة الإنجليزية 2", callback_data=f"{data}_en2")],
                [InlineKeyboardButton("مقدمة في منهجية البحث العلمي", callback_data=f"{data}_sr")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data=="shared_uo":
        await query.edit_message_text(
            text="📚 اختياري الجامعة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("الريادة والابداع", callback_data=f"{data}_spo"), InlineKeyboardButton("إسعافات أولية", callback_data=f"{data}_aid")],
                [InlineKeyboardButton("الرياضة والصحة", callback_data=f"{data}_hel"), InlineKeyboardButton("الفكر الإسلامي", callback_data=f"{data}_isl")],
                [InlineKeyboardButton("القانون في حياتنا", callback_data=f"{data}_law"), InlineKeyboardButton("تنشئة الأطفال", callback_data=f"{data}_chi")],
                [InlineKeyboardButton("حضارة إسلامية", callback_data=f"{data}_civ"), InlineKeyboardButton("حركة أسيرة", callback_data=f"{data}_asp")],
                [InlineKeyboardButton("مقدمة في هندسة السيارات", callback_data=f"{data}_car"), InlineKeyboardButton("مهارات التواصل المهني", callback_data=f"{data}_com")],
                [InlineKeyboardButton("مكافحة الفساد", callback_data=f"{data}_ant"), InlineKeyboardButton("قضايا معاصرة", callback_data=f"{data}_iss")],
                [InlineKeyboardButton("اللغة التركية", callback_data=f"{data}_tur"), InlineKeyboardButton("المكتبة وطرق البحث", callback_data=f"{data}_lib")],
                [InlineKeyboardButton("اللغة العبرية", callback_data=f"{data}_heb"), InlineKeyboardButton("تاريخ القدس", callback_data=f"{data}_jer")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="shared_subjects"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    
    elif data in ["cse", "me", "ee", "te", "ce"]:
        titles = {
            "cse": "💻 هندسة الحاسوب",
            "me": "⚙️ هندسة الميكانيك والميكاترونيكس",
            "ee": "⚡ الهندسة الكهربائية والأتمتة الصناعية",
            "te": "📡 هندسة الاتصالات",
            "ce": "🏗 هندسة البناء والهندسة المدنية"
        }

        await query.edit_message_text(
            text=titles[data],
            reply_markup=specialization_menu(data)
        )


    # ---- Subjects ----
    elif data.endswith("_subjects"):
        spec = data.replace("_subjects", "")
        await query.edit_message_text(
            text="      📘 اخـــــــتــــــر نـــــــوع الــــــمـــــواد:      ",
            reply_markup=subjects_menu(spec)
        )

    # ---- Subject lists (example implementation) ----
    elif data.endswith(("cse_dm")):
        await query.edit_message_text(
            text="📚 اختر مادة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("برمجة الحاسوب", callback_data=f"{data}_cpp"), InlineKeyboardButton("البرمجة الكينونية", callback_data=f"{data}_java"), InlineKeyboardButton("تركيب البيانات", callback_data=f"{data}_ds")],
                [InlineKeyboardButton("م. تركيب البيانات", callback_data=f"{data}_dslab"), InlineKeyboardButton("تراكيب الحوسبة المتقطعة", callback_data=f"{data}_dis")], 
                [InlineKeyboardButton("نظم تشغيل", callback_data=f"{data}_os"), InlineKeyboardButton("خوارزميات", callback_data=f"{data}_alg"), InlineKeyboardButton("قواعد البيانات", callback_data=f"{data}_db")],
                [InlineKeyboardButton("شبكات الحاسوب", callback_data=f"{data}_net"), InlineKeyboardButton("م. قواعد البيانات", callback_data=f"{data}_dblab")],
                [InlineKeyboardButton("معمارية الحاسوب", callback_data=f"{data}_arc"), InlineKeyboardButton("م. شبكات الحاسوب", callback_data=f"{data}_netlab")],
                [InlineKeyboardButton("تحليل وتصميم أنظمة المعلومات", callback_data=f"{data}_isad")],
                [InlineKeyboardButton("م. أسمبلي", callback_data=f"{data}_asslab"), InlineKeyboardButton("أسمبلي", callback_data=f"{data}_ass"), InlineKeyboardButton("هندسة برمجيات", callback_data=f"{data}_soft")],
                [InlineKeyboardButton("التصميم المنطقي عالي المستوى", callback_data=f"{data}_vhdl")],
                [InlineKeyboardButton("تقنيات الانترنت وتطبيقات الويب", callback_data=f"{data}_web")],
                [InlineKeyboardButton("الذكاء الاصطناعي", callback_data=f"{data}_ai"), InlineKeyboardButton("برمجة الشبكات", callback_data=f"{data}_netpro")],
                [InlineKeyboardButton("الدوائر الكهربائية", callback_data=f"{data}_cir"), InlineKeyboardButton("م. الدوائر الكهربائية", callback_data=f"{data}_cirlab")],
                [InlineKeyboardButton("إلكترونيات", callback_data=f"{data}_ele"), InlineKeyboardButton("م. إلكترونيات", callback_data=f"{data}_elelab")],
                [InlineKeyboardButton("تصميم الدوائر المنطقية", callback_data=f"{data}_dig")],
                [InlineKeyboardButton("م. تصميم الدوائر المنطقية", callback_data=f"{data}_diglab")],
                [InlineKeyboardButton("إلكترونيات رقمية", callback_data=f"{data}_dige"), InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_sig")],
                [InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", callback_data=f"{data}_pro")],
                [InlineKeyboardButton("أنظمة الاتصالات", callback_data=f"{data}_cs"), InlineKeyboardButton("معالجة الإشارات الرقمية", callback_data=f"{data}_dsp")],
                [InlineKeyboardButton("أنظمة التحكم 1", callback_data=f"{data}_con"), InlineKeyboardButton("تحليل عددي", callback_data=f"{data}_num")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="cse"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data.endswith(("cse_do")):
        await query.edit_message_text(
            text="📚 اختر مادة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("مواضيع متقدمة في قواعد البيانات", callback_data=f"{data}_adb")],
                [InlineKeyboardButton("أنظمة الألياف الضوئية", callback_data=f"{data}_fib")],
                [InlineKeyboardButton("التشفير وأمن الشبكات", callback_data=f"{data}_cs"), InlineKeyboardButton("تنجيم البيانات", callback_data=f"{data}_dm")],
                [InlineKeyboardButton("مواضيع خاصة في هندسة انظمة الحاسوب", callback_data=f"{data}_acse")],
                [InlineKeyboardButton("تعلم الآلة", callback_data=f"{data}_ml"), InlineKeyboardButton("أنماط التصميم", callback_data=f"{data}_dis")],
                [InlineKeyboardButton("نظرية المعلومات والترميز (كودينج)", callback_data=f"{data}_cod")],
                [InlineKeyboardButton("المجسات ومحولات الطاقة (سنسور)", callback_data=f"{data}_sen")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="cse"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
        
    elif data.endswith(("te_dm")):
        await query.edit_message_text(
            text="📚 اختر مادة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("م. متحكمات دقيقة", callback_data=f"{data}_mcl"), InlineKeyboardButton("متحكمات دقيقة", callback_data=f"{data}_mic")],
                [InlineKeyboardButton("م. تصميم الدوائر المنطقية", callback_data=f"{data}_dll"), InlineKeyboardButton("تصميم الدوائر المنطقية", callback_data=f"{data}_dld")],
                [InlineKeyboardButton("م. إلكترونيات", callback_data=f"{data}_lel"), InlineKeyboardButton("إلكترونيات", callback_data=f"{data}_ele")],
                [InlineKeyboardButton("م. أنظمة تحكم 1", callback_data=f"{data}_lcl"), InlineKeyboardButton("أنظمة تحكم 1", callback_data=f"{data}_ctl")],
                [InlineKeyboardButton("م. دوائر كهربائية 1", callback_data=f"{data}_lec"), InlineKeyboardButton("دوائر كهربائية 1", callback_data=f"{data}_ec1")],
                [InlineKeyboardButton("م. دوائر كهربائية 2", callback_data=f"{data}_lc2"), InlineKeyboardButton("دوائر كهربائية 2", callback_data=f"{data}_ec2")],
                [InlineKeyboardButton("الاحتمالات والمتغيرات العشوائية", callback_data=f"{data}_prb")],
                [InlineKeyboardButton("اتصالات تماثلية", callback_data=f"{data}_acm"), InlineKeyboardButton("اتصالات رقمية", callback_data=f"{data}_dcm")],
                [InlineKeyboardButton("كهرومغناطيسية", callback_data=f"{data}_emg"), InlineKeyboardButton("الإشارات والنظم", callback_data=f"{data}_sig")],
                [InlineKeyboardButton("إلكترونيات متقدمة للاتصالات", callback_data=f"{data}_aec")],
                [InlineKeyboardButton("برمجة حاسوب", callback_data=f"{data}_prg"), InlineKeyboardButton("شبكات حاسوب", callback_data=f"{data}_net")],
                [InlineKeyboardButton("الصوتيات والأمواج الكهرومغناطيسية", callback_data=f"{data}_aew")],
                [InlineKeyboardButton("الهوائيات وانتشار الأمواج", callback_data=f"{data}_ant")],
                [InlineKeyboardButton("المجسات ومحولات الطاقة", callback_data=f"{data}_spc")],
                [InlineKeyboardButton("تحليل عددي", callback_data=f"{data}_num"), InlineKeyboardButton("أنظمة الألياف الضوئية", callback_data=f"{data}_ofs")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="te"),
                     InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )
    elif data.endswith(("te_do")):
        await query.edit_message_text(
            text="📚 اختر مادة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("تقنيات الإنترنت وتطبيقات الويب", callback_data=f"{data}_web")],
                [InlineKeyboardButton("تركيب بيانات", callback_data=f"{data}_db"), InlineKeyboardButton("البرمجة الكينونية", callback_data=f"{data}_oop")],
                [InlineKeyboardButton("هندسة البرمجيات", callback_data=f"{data}_swe")],
                [InlineKeyboardButton("نظرية المعلومات والترميز (كودينج)", callback_data=f"{data}_cod")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="te"),
                 InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data in SUBJECT_LINKS:
        await query.message.reply_text(
            f"{SUBJECT_LINKS[data]}"
        )

    # ---- Roadmaps ----
    elif data == "cse_roadmaps":
        keyboard = [
            [InlineKeyboardButton("🤖 AI & Machine Learning", callback_data="cse_rm_ai")],
            [InlineKeyboardButton("📊 Data Science", callback_data="cse_rm_ds"), InlineKeyboardButton("🤖 Robotics", callback_data="cse_rm_robotics")],
            [InlineKeyboardButton("🔐 Cybersecurity", callback_data="cse_rm_cyber"), InlineKeyboardButton("🌐 Full Stack Developer", callback_data="cse_rm_fullstack")],
            [InlineKeyboardButton("🎨 Frontend", callback_data="cse_rm_frontend"), InlineKeyboardButton("🧠 Backend", callback_data="cse_rm_backend")],
            [InlineKeyboardButton("📱 Mobile Application", callback_data="cse_rm_mobile"), InlineKeyboardButton("🖌 UI / UX", callback_data="cse_rm_uiux")],
            [InlineKeyboardButton("🧪 QA", callback_data="cse_rm_qa"), InlineKeyboardButton("🎮 Game Developer", callback_data="cse_rm_game")],
            [InlineKeyboardButton("⚙ Low Level Programming", callback_data="cse_rm_lowlevel")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="cse"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
        ]

        await query.edit_message_text(
            text="🗺 Roadmaps – هندسة الحاسوب",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data in ROADMAP_LINKS:
        await query.message.reply_text(
            f"{ROADMAP_LINKS[data]}"
    )

        # await query.message.reply_text(
        #     "🗺 Roadmaps – هندسة الحاسوب",
        #     reply_markup=InlineKeyboardMarkup([
        #         [InlineKeyboardButton("🔙 رجوع", callback_data="cse_roadmaps"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
        #     ])
        # )

    # ---- FAQ ----
    elif data == "faq":
        keyboard = [
            [InlineKeyboardButton("🏫 عن الجامعة", callback_data="faq_university"), InlineKeyboardButton("🎓 عن المنح", callback_data="faq_scholarships"), InlineKeyboardButton("👨‍🏫 عن المدرسين", callback_data="faq_teachers")],
            [InlineKeyboardButton("📚 عن الدراسة وطرقها", callback_data="faq_study"), InlineKeyboardButton("🐣 أسئلة سنافر", callback_data="faq_freshmen"), InlineKeyboardButton("💡 نصائح", callback_data="faq_tips")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]

        await query.edit_message_text(
            text="❓ الأسئلة الشائعة:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "faq_university":
        await query.edit_message_text(
            text="🏫 عن الجامعة:\n\n"
                 "س: هل الجامعة معترف بها؟\n"
                 "ج: نعم، الجامعة معترف بها رسميًا.\n\n"
                 "س: أين تقع الجامعة؟\n"
                 "ج: يتم تحديد الموقع حسب الكلية.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_scholarships":
        await query.edit_message_text(
            text="🎓 عن المنح:\n\n"
                 "س: هل توجد منح؟\n"
                 "ج: نعم، توجد منح تفوق ومنح دعم.\n\n"
                 "س: كيف أقدم على منحة؟\n"
                 "ج: عبر شؤون الطلاب.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_study":
        await query.edit_message_text(
            text="📚 عن الدراسة وطرقها:\n\n"
                 "س: هل الدراسة صعبة؟\n"
                 "ج: تحتاج التزام وتنظيم وقت.\n\n"
                 "س: هل المحاضرات مسجلة؟\n"
                 "ج: يعتمد على المادة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_teachers":
        await query.edit_message_text(
            text="👨‍🏫 عن المدرسين:\n\n"
                 "س: هل المدرسون متعاونون؟\n"
                 "ج: أغلبهم متعاونون داخل المحاضرات.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_freshmen":
        await query.edit_message_text(
            text="🐣 أسئلة سنافر:\n\n"
                 "س: ماذا أدرس أولًا؟\n"
                 "ج: ركز على الأساسيات.\n\n"
                 "س: كيف أنظم وقتي؟\n"
                 "ج: جدول أسبوعي بسيط.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    elif data == "faq_tips":
        await query.edit_message_text(
            text="💡 نصائح:\n\n"
                 "• لا تؤجل الدراسة\n"
                 "• تابع التلاخيص\n"
                 "• اسأل ولا تتردد",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="faq"), InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")]
            ])
        )

    # ---- Back to main ----
    elif data == "back_main":
        await query.edit_message_text(
            text="👋 أهلاً بك في بوت الهندسة الجامعية\n\n"
            "📌 **طريقة استخدام البوت:**\n"
            "• البوت يعمل بالكامل عبر الأزرار.\n"
            "• اختر تخصصك من القائمة الرئيسية.\n"
            "• ادخل إلى قسم المواد ثم اختر نوع المادة.\n"
            "• داخل كل مادة ستجد التلاخيص، الشروحات، الكتب، الامتحانات وغيرها.\n"
            "• يمكنك دائمًا الرجوع باستخدام زر (رجوع).\n\n"
            "💡 لأي ملاحظات أو اقتراحات استخدم الأمر:\n"
            "/note\n\n"
            "👇 اختر من القائمة:",
            reply_markup=main_menu_keyboard()
        )
    # ---- Remove the sent note ----
    elif data == "delete_note":
        msg_id = context.user_data.get("last_note_msg_id")
        note_time = context.user_data.get("note_time")

        if not msg_id or not note_time:
            await query.answer("❌ لا توجد ملاحظة للحذف", show_alert=True)
            return

        if time.time() - note_time > 5:
            await query.answer("⏱ انتهت مهلة الحذف", show_alert=True)
            await query.message.edit_text("❌ انتهت مهلة حذف الملاحظة.")
            return

        await context.bot.delete_message(
            chat_id=TARGET_CHAT_ID,
            message_id=msg_id
        )

        await query.message.edit_text("🗑 تم حذف الملاحظة بنجاح.")
# =========================
# Notes forwarding
# =========================

TARGET_CHAT_ID = -1002905917338

async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_note"] = True
    await update.message.reply_text("✍️ أرسل الملاحظة الآن:")


async def handle_note_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_note"):
        user = update.effective_user
        note_text = update.message.text
        username_text = f"@{user.username}" if user.username else "—"
        full_message = (
            "📩 ملاحظة جديدة\n\n"
            f"📝 النص:\n{note_text}\n\n"
            "──────────────\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🆔 Telegram ID: {user.id}\n"
             f"🔗 Username: {username_text}"
        )

        sent_msg = await context.bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=full_message
        )

        # حفظ بيانات الحذف
        context.user_data["last_note_msg_id"] = sent_msg.message_id
        context.user_data["note_time"] = time.time()

        await update.message.reply_text(
    "✅ تم إرسال الملاحظة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑 حذف الملاحظة", callback_data="delete_note")]
            ])
)
        context.user_data["waiting_for_note"] = False


# =========================
# Main
# =========================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("inst", inst))
    # app.add_handler(CommandHandler("bots", bots))
    app.add_handler(CommandHandler("note", note_command))

    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
