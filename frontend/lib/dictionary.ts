export const dictionary = {
    common: {
        start: "Hesabla",
        calculate: "Vergi Hesabla",
        legalBasis: "Hüquqi Əsas",
        pilotVersion: "Pilot Versiya",
        consulProfessional: "Bu alət yalnız məlumat xarakterlidir. Rəsmi məlumat üçün peşəkar məsləhətçi ilə əlaqə saxlayın.",
        basedOn: "Əsaslanır:",
        taxCode: "Azərbaycan Respublikasının Vergi Məcəlləsi",
        back: "Geri",
        continue: "Davam et",
        step: "Addım",
        loading: "Yüklənir...",
        eg: "məs.,",
    },
    home: {
        hero: {
            title: "Azərbaycan Sadələşdirilmiş Vergi Kalkulyatoru",
            subtitle: "Sadələşdirilmiş vergi öhdəliyinizi və hüququnuzu bir neçə addımda müəyyən edin.",
            cta: "İndi Başla",
            note: "10-15 sualla vergi statusunuzu dəqiqləşdirin",
        },
        features: {
            eligibility: {
                title: "Uyğunluq Yoxlaması",
                desc: "Sadələşdirilmiş vergi ödəyicisi olmaq hüququnuzu ani müəyyən edin"
            },
            calculation: {
                title: "Dəqiq Hesablama",
                desc: "Gəlirinizə əsasən ödəyəcəyiniz vergi məbləğini hesablayın (Bakı: 2%, Regionlar: 2%)"
            },
            legal: {
                title: "Qanunvericilik",
                desc: "Hər bir addım Vergi Məcəlləsinin müvafiq maddələrinə istinad edir"
            }
        }
    },
    layout: {
        header: {
            title: "Sadələşdirilmiş Vergi",
            subtitle: "Kalkulyatoru"
        },
        footer: {
            rights: "Bütün hüquqlar qorunur"
        }
    },
    calculator: {
        steps: {
            vat: "ƏDV Statusu",
            route: "Fəaliyyət Növü",
            turnover: "Dövriyyə",
            disqualifiers: "Uyğunluq",
            result: "Nəticə"
        },
        vat: {
            question: "ƏDV qeydiyyatınız varmı?",
            tooltip: "ƏDV qeydiyyatında olan vergi ödəyiciləri sadələşdirilmiş vergi rejimindən istifadə edə bilməzlər.",
            no: {
                label: "Xeyr, ƏDV qeydiyyatında deyiləm",
                subLabel: "Sadələşdirilmiş vergi rejimi üçün uyğun ola bilərsiniz",
                badge: "Uyğun"
            },
            yes: {
                label: "Bəli, ƏDV qeydiyyatındayam",
                subLabel: "ƏDV ödəyiciləri sadələşdirilmiş vergidən istifadə edə bilməz (Maddə 218.1.1)",
                badge: "Uyğun deyil"
            },
            error: "Zəhmət olmasa ƏDV qeydiyyatı sualına cavab verin"
        },
        activities: {
            question: "Aşağıdakı fəaliyyətlərdən hansılar sizə aiddir?",
            tooltip: "Bu xüsusi kateqoriyalar dövriyyə həddindən asılı olmayaraq avtomatik olaraq sadələşdirilmiş vergiyə uyğundur.",
            none: "Yuxarıdakılardan heç biri",
            noneDesc: "Uyğunluq dövriyyə həddindən asılıdır (200,000 AZN)",
            items: {
                transport: { label: "Sərnişin daşıma/taksi", desc: "Maddə 218.4.1" },
                betting: { label: "Mərc/lotereya", desc: "Maddə 218.4.2" },
                property: { label: "Özümə məxsus daşınmaz əmlakın satışı", desc: "Maddə 218.4.3" },
                fixed: { label: "220.10 üzrə işçisi olmayan sabit fəaliyyət", desc: "Maddə 218.4.4" },
                land: { label: "Özümə məxsus torpağın satışı", desc: "Maddə 218.4.5" }
            },
            propertyExemption: {
                question: "Bu yaşayış sahəsi Vergi Məcəlləsinin 218-1.1.5-ci maddəsinə əsasən vergidən azaddırmı?",
                tooltip: "Müəyyən əmlak köçürmələri sadələşdirilmiş vergidən tam azaddır.",
                options: {
                    registered: { label: "Həmin ünvanda ən azı 3 təqvim ili qeydiyyatda olmuşam", desc: "Maddə 218-1.1.5.1" },
                    proof: { label: "3+ il yaşadığımı sübut edə bilirəm VƏ yalnız bir yaşayış sahəm var", desc: "Maddə 218-1.1.5.1-1" },
                    gift: { label: "Bu ailə üzvündən bağışlama və ya vərəsəlikdir", desc: "Maddə 102.1.3.2" },
                    none: { label: "Yuxarıdakılardan heç biri uyğun deyil", desc: "30 m² güzəşti tətbiq ediləcək" },
                },
                details: {
                    title: "Əmlak Məlumatları",
                    type: "Əmlak növü",
                    area: "Sahə (m²)",
                    zone: "Yerləşmə zonası",
                    types: { residential: "Yaşayış sahəsi", non_residential: "Qeyri-yaşayış sahəsi" },
                    zones: {
                        baku_center: "Bakı Mərkəzi (Zona 1)",
                        baku_other: "Bakı Digər (Zona 2)",
                        sumgait_ganja_lankaran: "Sumqayıt / Gəncə / Lənkəran",
                        other_cities: "Digər şəhərlər",
                        rural: "Kənd yerləri"
                    }
                }
            },
            trade: {
                question: "Ticarət və/və ya ictimai iaşə ilə məşğulsunuzmu?",
                tooltip: "200 min manatdan yuxarı dövriyyəsi olan ticarət və iaşə fəaliyyətlərinin fərqli vergi dərəcələri var.",
                retail: { label: "Ticarət (pərakəndə və ya topdan)" },
                catering: { label: "İctimai iaşə" }
            }
        },
        turnover: {
            question: "Son 12 ay üçün dövriyyə detallarınızı daxil edin:",
            tooltip: "200.000 AZN testi ƏDV fəsli qaydaları əsasında hesablanır. ƏDV-dən azad axınları daxil etməyin.",
            warning: {
                title: "Dövriyyə Həddi: 200,000 AZN",
                desc: "Əgər tənzimlənmiş dövriyyəniz <strong>200,000 AZN</strong>-i keçirsə, sadələşdirilmiş vergi rejimindən istifadə hüququnuzu itirirsiniz (Maddə 218.1.1)."
            },
            info: {
                title: "Hesablama Qaydası",
                desc: "Yalnız ƏDV-yə cəlb olunan əməliyyatlar nəzərə alınır. POS-terminal vasitəsilə nağdsız dövriyyə <strong>50%</strong> (0.5 əmsalı) ilə hesablanır."
            },
            inputs: {
                gross: { label: "Ümumi Dövriyyə (AZN)", desc: "Son 12 ay üçün ümumi gəlir" },
                exempt: { label: "ƏDV-dən Azad Dövriyyə (AZN)", desc: "Maddə 164 üzrə azad olunanlar" },
                posRetail: { label: "POS Pərakəndə Dövriyyəsi (AZN)", desc: "Qeydiyyatsız şəxslərə nağdsız satış", sectionTitle: "POS Nağdsız Dövriyyə (0.5 əmsalı üçün)" },
                posServices: { label: "POS Xidmət Dövriyyəsi (AZN)", desc: "Qeydiyyatsız şəxslərə nağdsız xidmət" }
            }
        },
        disqualifiers: {
            info: {
                title: "Uyğunluq Yoxlaması",
                desc: "Müəyyən fəaliyyət növləri sadələşdirilmiş vergi rejimindən istifadəni məhdudlaşdırır. 'Uyğun deyil' işarəli seçimlər sizi diskvalifikasiya edəcək."
            },
            excise: {
                question: "Aksizli və ya mütləq markalanan mallar istehsal edirsinizmi?",
                no: "Xeyr",
                yes: "Bəli",
                disqualify: "Aksizli mal istehsalçıları sadələşdirilmiş vergidən istifadə edə bilməz"
            },
            financial: {
                question: "Aşağıdakı maliyyə qurumlarından birisinizmi?",
                credit: "Kredit təşkilatı",
                insurance: "Sığorta bazarının peşəkar iştirakçısı",
                investment: "İnvestisiya fondu və ya meneceri",
                securities: "Qiymətli kağızlar bazarının lisenziyalı iştirakçısı",
                pawnshop: "Lombard"
            },
            income: {
                question: "İcarə və ya royalti gəliri əldə edirsinizmi?",
                rental: "İcarə gəliri",
                royalty: "Royalti gəliri"
            },
            license: {
                question: "Lisenziya tələb edən hər hansı fəaliyyətlə məşğulsunuzmu?",
                tooltip: "Lisenziyalı fəaliyyətlər ümumiyyətlə sadələşdirilmiş vergidən istifadə edə bilməz.",
                exception: "Yalnız icbari sığorta müqavilələri üzrə xidmət göstərirəm",
                items: {
                    medical: "Özəl tibb fəaliyyəti",
                    education: "Təhsil fəaliyyəti",
                    comm: "Rabitə xidmətləri",
                    fire: "Yanğından mühafizə fəaliyyəti",
                    survey: "Mühəndis axtarışları",
                    construction: "Tikinti-quraşdırma işləri",
                    design: "Layihələndirmə",
                    other: "Digər lisenziyalı fəaliyyət"
                }
            },
            wholesale: {
                question: "Topdan ticarət edirsinizmi?",
                tooltip: "Topdan ticarət ümumiyyətlə qadağandır, lakin müəyyən istisnalar mövcuddur.",
                no: "Xeyr",
                yes: "Bəli",
                ratio: "Elektron qaimə ilə rəsmiləşdirilən əməliyyatların faizi",
                disqualify: "Topdan satış rəsmiləşdirməsi 30%-dən yuxarı olmalıdır"
            },
            goods: {
                question: "Qızıl, zərgərlik, almaz, xəz və ya dəri məmulatları satırsınızmı?",
                gold: "Qızıl və zərgərlik",
                leather: "Xəz və dəri məmulatları"
            },
            production: {
                question: "İstehsal fəaliyyəti ilə məşğulsunuzmu (kənd təsərrüfatı istisna)?",
                label: "İstehsal fəaliyyəti",
                employees: "Orta rüblük işçi sayı",
                disqualify: "10-dan çox işçisi olan istehsalçılar sadələşdirilmiş vergidən istifadə edə bilməz"
            },
            b2b: {
                question: "Vergi ödəyicilərinə (B2B) iş və ya xidmət göstərirsinizmi?",
                no: "Xeyr",
                yes: "Bəli",
                ratio: "Elektron qaimə ilə rəsmiləşdirilən əməliyyatların faizi",
                disqualify: "B2B xidmətlərinin rəsmiləşdirməsi 30%-dən yuxarı olmalıdır"
            },
            entity: {
                question: "Dövlət orqanı və ya publik hüquqi şəxssinizmi?",
                label: "Dövlət orqanı / PHŞ",
                disqualify: "Publik hüquqi şəxslər sadələşdirilmiş vergidən istifadə edə bilməz"
            }
        },
        results: {
            eligible: {
                title: "Uyğundur",
                desc: "Sadələşdirilmiş vergi üçün uyğundur",
                taxAmount: "Vergi Məbləği",
                exempt: "Azad (0 vergi)",
                route: "Marşrut"
            },
            notEligible: {
                title: "Uyğun Deyil",
                desc: "Sadələşdirilmiş vergi üçün uyğun deyil",
                debug: "Xəta İzi (İlk Uyğunsuzluq)"
            },
            details: {
                button: "Təfərrüatlar və Hüquqi İstinadlar",
                breakdown: "Hesablama Təfərrüatları",
                taxBase: "Vergi Bazası",
                taxRate: "Vergi Dərəcəsi",
                exemptions: "Tətbiq Edilən Güzəştlər",
                citations: "Hüquqi İstinadlar",
                article: "Maddə"
            },
            restart: "Yenidən Başla"
        }
    }
} as const;
