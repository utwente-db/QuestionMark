# This file contains the benchmark queries in the dialect of MayBMS.
# Go to queries_pseudocode.py for an overview of the queries available for this benchmark.


MAYBMS_QUERIES_DICT = {

    # ====== TEST THE CONNECTION ==================================================================== #

    # Testing the connection
    'test_1': """
    SELECT id
    FROM offers
    LIMIT 10;
    """,

    # ====== INSIGHT QUERIES ========================================================================== #

    # Retrieve the full dataset, gain insight in data structure.
    'insight_1': """
    SELECT * 
    FROM offers;
    """,

    # Provide insight into the dataset.
    'insight_2': """
    SELECT COUNT(*) as records, 
        COUNT(DISTINCT(id)) as offers, 
        COUNT(DISTINCT(cluster_id)) as clusters
    FROM offers_setup;
    """,

    # Provide insight into the distribution of cluster volumes.
    'insight_3': """
    SELECT cluster_size, COUNT(cluster_size) as amount
    FROM (
        SELECT COUNT(DISTINCT(id)) as cluster_size
        FROM offers_setup
        GROUP BY cluster_id
    ) as cluster_sizes
    GROUP BY cluster_size
    ORDER BY cluster_size ASC;
    """,

    # Gets the percentage of certain clusters.
    'insight_4': """
    SELECT ROUND(all_certain::decimal / all_offers::decimal, 4) * 100 AS certain_percentage
    FROM (
        SELECT COUNT(id) AS all_offers
        FROM offers_setup
    ) AS count_all, (
        SELECT COUNT(id) AS all_certain
        FROM (
            SELECT id, tconf() AS confidence
            FROM offers
        ) AS confidences
        WHERE confidence = 1
    ) AS count_cert;
    """,

    # Get the id of the offers with sentence 'w8=1'.
    'insight_5': """
    SELECT id, tconf(*), _v0
    FROM offers
    WHERE _v1 = 52379
    AND _d1 = 548185;
    """,

    # Get the average probability of the dataset.
    'insight_6': """ 
    SELECT AVG(tconf()) * 100 AS certainty_of_the_dataset
    FROM offers;
    """,



    # ====== PROBABILISTIC QUERIES ========================================================================== #

    # Get offers with the probability of their occurrence.
    'probabilistic_1': """
    SELECT round(conf()::NUMERIC, 4) AS probability, *
    FROM offers
    GROUP BY id
    ORDER BY probability DESC;
    """,

    # Gets the expected count of the categories.
    'probabilistic_2': """
    SELECT category, ECOUNT() AS expected_count
    FROM offers
    GROUP BY category
    ORDER BY expected_count DESC;
    """,

    # Gets the expected sum of the product ids per cluster
    'probabilistic_3': """
    SELECT cluster_id, esum(id), COUNT(id) AS number_of_offers
    FROM offers
    GROUP BY cluster_id
    ORDER BY number_of_offers DESC;
    """,

    # Gets the sentence and probability for the categories
    'probabilistic_4': """
    SELECT category, conf() AS probability
    FROM offers
    GROUP BY category
    ORDER BY probability DESC;
    """,

    # Search Ford of web shop, where most probable product should be returned
    'probabilistic_5': """ 
    SELECT *, round(tconf()::NUMERIC, 4) AS probability
    FROM offers
    WHERE cluster_id IN (
        SELECT cluster_id
        FROM offers_setup 
        WHERE title LIKE '%ford%' 
        OR description LIKE '%ford%'
    ) 
    ORDER BY probability DESC 
    LIMIT 1;
    """,

    # Returns all offers with high uncertainty for human check
    'probabilistic_6': """
    SELECT id, cluster_id, brand, category, identifiers
    FROM offers
    WHERE title LIKE '%ford%' 
    OR description LIKE '%ford%'
    AND tconf() > 0.40
    AND tconf() < 0.60;
    """,



    # ====== INSERT, UPDATE, DELETE ================================================================= #

    'IUD_1_rollback': """
    INSERT INTO offers_setup (id, cluster_id, title, brand, category, description, price, identifiers, keyvaluepairs, spectablecontent, world_prob, attribute_prob)
        VALUES(-464, 77, 'hp pavilion 15 b105tx ultrabook lcd ekran panel dataservis te 439654 rq 5489 net', 'None', 'Computers_and_Accessories', 'y zde y z uyum garant s detaylari n tiklayiniz 100 uyum garant s y zde y z uyum garant s ncelemekte oldu unuz r nde kopyala yap t r y ntemiyle hayali r n olu turan yap lardan korunmak amac yla temsili resim kullan lm t r yay nlad m z t m uyumluluk bilgileri uzman r n y neticilerimiz taraf ndan yap lan test ve kontroller neticesinde elde edilmekte ve uyum garantisi sa land ktan sonra yay na sunulmaktad r bu r n belirtilen model par a kodu ve r n a klamalar er evesinde cihaz n zla y zde y z uyumludur stisnai durumlarda uyumsuzlu un ispatlanmas ko uluyla hatal uyumsuz r n n geri g nderilmesi ve do ru r n n sevk edilmesiyle ilgili t m kargo giderleri firmam za aittir geri g nderimin anla mal oldu umuz kargo firmas ile yap lmas gerekmektedir durumu yeni r n boyut 15 6 z n rl k wxga hd piksel 1366 x 768 y zey parlak ayd nlatma led notlar', 'None', '[{/sku: [439654rq5489]}]', '{bulundu u depolar: stok merkez: merkez outlet: kadik y 0 216 550 71 42: r n kodu: 439654 rq 5489 fiyat: 55 12 usd kdv 214 31 tl kdv garanti: 12 ay stok: var}', 'bulundu u depolar stok merkez merkez outlet kadik y 0 216 550 71 42 g ncellenme 18 11 2017 14 03 50 r n kodu 439654 rq 5489 fiyat 55 12 usd kdv 214 31 tl kdv kdv dahil 65 04 usd 252 88 tl garanti 12 ay stok var', 0.42911, 0.629),
              (-466, 77, 'hp pavilion 15 n015ax batarya pil retro 8cell dataservis te 421745 ol 7989 net', 'None', 'Computers_and_Accessories', 'y zde y z uyum garant s detaylari n tiklayiniz 100 uyum garant s y zde y z uyum garant s ncelemekte oldu unuz r nde kopyala yap t r y ntemiyle hayali r n olu turan yap lardan korunmak amac yla temsili resim kullan lm t r yay nlad m z t m uyumluluk bilgileri uzman r n y neticilerimiz taraf ndan yap lan test ve kontroller neticesinde elde edilmekte ve uyum garantisi sa land ktan sonra yay na sunulmaktad r bu r n belirtilen model par a kodu ve r n a klamalar er evesinde cihaz n zla y zde y z uyumludur stisnai durumlarda uyumsuzlu un ispatlanmas ko uluyla hatal uyumsuz r n n geri g nderilmesi ve do ru r n n sevk edilmesiyle ilgili t m kargo giderleri firmam za aittir geri g nderimin anla mal oldu umuz kargo firmas ile yap lmas gerekmektedir marka retro durumu yeni r n h creler cells li ion 8 cell voltaj v 14 4 kapasite mah 4400 g wh 63 renk siyah notlar y ksek kapasite ve ilave h crelerden dolay ebatlar standart bataryaya g re daha b y k olabilir bu bataryan n volt v ve amper saat mah de erleri kullanmakta oldu unuz bataryadan farkl olabilir bu durum 100 uyum a s ndan hi bir sorun te kil etmemektedir volt v bataryan n i erisindeki h cre cell say s ile ilgilidir rne in 14 4v 14 8v bir batarya 4 8 adet silindirik li ion h cre i erir 10 8v 11 1v bir batarya ise 3 6 adet silindirik li ion h cre i erir amper saat mah bataryan n kapasitesini ifade etmektedir rne in yeni bir 5200mah batarya cihaz n z yakla k 2 5 saat al t r yorsa yeni bir 4400mah batarya ayn cihaz yakla k 2 saat s re ile al t racakt r watt saat wh bataryan n g c n ifade eder wh v x mah eklinde hesaplan r bataryan z n uzun m rl olmas in bunlara dikkat batarya kullan m ekli pil h crelerinin mr a s ndan ok nemlidir bir notebook bataryas n maksimum verimle uzun m rl kullanmak i in a a daki hususlara dikkat edilmesi gerekir 1 bataryay s rekli canl tutunuz haftada en az bir kez de arj ve arj i lemini ger ekle tiriniz uzun s re arj de arj i lemi yap lmazsa h creler enerji depolama zelli ini yitirmeye ba larlar 2 notebooku m mk n olduk a batarya ile kullan n z g adapt r ile al rken bataryan n 100 dolu oldu u ikaz n al nca adapt r ba lant s n kesiniz arj adapt r ile uzun s reli kullan mlarda genellikle notebookun desktop olarak kullan ld durumlar bataryan n arj de arj i lemi ihmal edilebilmektedir 3 bataryadaki enerji seviyesinin 5 in alt na d mesine izin vermeyiniz notebookunuzdaki g se enekleri ayarlar ndan kritik arj seviyesini d zenleyebilirsiniz batarya enerji seviyesi 0 mertebesine indi inde pillerin ilk arj almas g le mekte ve ayr ca enerjisinin asla kesilmemesi gereken batarya i devresi bozulabilmektedir bu durumda pil h creleri sa lam olsa bile batarya sa l kl bir ekilde al mayacakt r 4 notebookunuzun so utma sisteminin sa l kl bir ekilde al p al mad na dikkat ediniz aksi takdirde a r s dan dolay pil h creleri zarar g r p zelliklerini yitirebilirler 5 batarya kullan m zaruri de il ise ve bataryan n y llarca sa l kl kalmas isteniyorsa 100 dolu bir ekilde kuru bir ortamda muhafaza edilmeli haftada bir kez de arj arj i lemi uygulanarak canl tutulmal d r 6 notebook al r durumda iken batarya s kme takma i lemi yap lmamal d r hem notebook hem de bataryan n s hhati a s ndan bu konuya dikkat edilmelidir 7 bataryan n notebooka ba lant noktalar kesinlikle k sa devre edilmemelidir 8 batarya kesinlikle nemden s v temas ndan ve a r s dan korunmal d r 9 notebooka herhangi bir ekilde s v temas oldu unda ilk olarak enerji kesilip batarya s k lmelidir s v temas n n notebooka verebilece i zararlar en aza indirmek bu ekilde m mk n olacakt r 10 batarya yuvas na tam oturmuyor ise zorlanmamal fiziksel hasarlardan ka nmal ve bir servise ba vurulmal d r 11 notebook mutlaka arkas nda yazan input volt ve amper de erlerini asgaride ta yan yeterli g seviyesine watt sahip bir g adapt r ile kullan lmal d r aksi durumda notebook al sa bile batarya arj ger ekle mez ve h creler zamanla canl l klar n yitirirler 12 batarya kullan m s resi notebookun o anda ne kadar enerji harcad ile alakal d r notebook zerinde enerji harcayan bir ok donan m mevcuttur cpu vga chip fanlar speakerlar hdd ve optik s r c motoru wireless lan bluetooth usb ayg tlar vs bu donan mlar n de i ik kullan m kombinasyonlar farkl s relerde batarya mr anlam na gelmektedir dolay s yla bataryan zdan her ekilde ayn kullan m s resini beklemeyiniz bataryan z sadece internette dola rken 3 saat dayan yorsa 3d oyun oynarken vga chip cpu fanlar speakerlar yo un olarak devrede 1 5 saat veya y ksek sesle cd den m zik dinlerken optik s r c motoru speakerlar yo un olarak devrede 2 saat dayanmas normaldir 13 g adapt r notebooka ba l iken batarya enerji seviyesi 1 puan bile ilerlemiyorsa ncelikle notebookun batarya arj devresinin sa lam olup olmad kontrol edilmeli ettirilmelidir batarya arj devresi ar zal ise gereksiz yere yeni bir batarya sat n alm olabilirsiniz 14 batarya mr azald nda kesinlikle oklama y ntemine ba vurmay n z bataryan z n kalan mr n de bu ekilde t ketmi olacaks n z oklama bataryaya ge ici bir kapasite kazand r r ve k sa s re sonra batarya tamamen mr n yitirir 15 batarya mr azald nda veya batarya arj olmad nda pil h crelerini de i tirmek yayg n olarak kullan lan bir y ntemdir ancak o unlukla zaman para ve kaynak israf ile sonu lanmaktad r h cre de i imi bilin li ve profesyonelce yap ld nda verimli olabilmekte batarya i devresi sa lam olmak kayd yla ancak bu i lemin maliyeti de yeni bir batarya bedeline yakla maktad r 16 batarya ar zalar n n b y k bir k sm batarya i erisindeki kontrol devresi ile ilgilidir bunun bir ok sebebi olabilir adapt r ar zas yanl adapt r kullan m elektrik seviyesindeki dengesizlikler elektronik komponent m rleri vs ancak h cre de i imi y ntemi bataryadaki bu problemi ortadan kald rmaz yeni bir batarya almak ka n lmazd r 17 yeni al nan bir bataryan n ilk kullan m ok nemlidir ve bataryan n gelecekteki mr ve performans b y k oranda ilk kullan mda belirlenir yeni ald n z bataryay ilk olarak u ekilde kullan n z batarya notebooka ba l ve notebook kapal vaziyette iken cihaz yakla k 10 12 saat arjda b rak n z notebooku al t rd n zda bataryan n 100 dolmu oldu unu g receksiniz bataryay 5 seviyesine kadar de arj edip tekrar 100 oluncaya kadar arj ediniz bu i lemi 4 5 kez tekrar ediniz bataryan z gelecekteki kullan m i in en verimli ekilde haz rlanm olacakt r', 'None', '[{/sku: [421745ol7989]}]', '{r n kodu: 421745 ol 7989, fiyat: 24 64 usd kdv 95 80 tl kdv, garanti: 24 ay, stok: var, marka: retro, durumu: yeni r n, h creler cells: li ion 8 cell, voltaj v: 14 4, kapasite mah: 4400, g wh: 63, renk: siyah, notlar: y ksek kapasite ve ilave h crelerden dolay ebatlar standart bataryaya g re daha b y k olabilir}', 'r n kodu 421745 ol 7989 fiyat 24 64 usd kdv 95 80 tl kdv kdv dahil 29 08 usd 113 04 tl garanti 24 ay stok var marka retro durumu yeni r n h creler cells li ion 8 cell voltaj v 14 4 kapasite mah 4400 g wh 63 renk siyah notlar y ksek kapasite ve ilave h crelerden dolay ebatlar standart bataryaya g re daha b y k olabilir', 0.5, 0.246),
              (-468, 77, 'hp pavilion dv6 3310st klavye i kl 321447 zc 2321 dataservis net', 'None', 'Computers_and_Accessories', 'y zde y z uyum garant s detaylari n tiklayiniz 100 uyum garant s y zde y z uyum garant s ncelemekte oldu unuz r nde kopyala yap t r y ntemiyle hayali r n olu turan yap lardan korunmak amac yla temsili resim kullan lm t r yay nlad m z t m uyumluluk bilgileri uzman r n y neticilerimiz taraf ndan yap lan test ve kontroller neticesinde elde edilmekte ve uyum garantisi sa land ktan sonra yay na sunulmaktad r bu r n belirtilen model par a kodu ve r n a klamalar er evesinde cihaz n zla y zde y z uyumludur stisnai durumlarda uyumsuzlu un ispatlanmas ko uluyla hatal uyumsuz r n n geri g nderilmesi ve do ru r n n sevk edilmesiyle ilgili t m kargo giderleri firmam za aittir geri g nderimin anla mal oldu umuz kargo firmas ile yap lmas gerekmektedir durumu yeni r n dil q t rk e renk siyah notlar led ayd nlatmal', 'None', '[{/sku: [321447zc2321]}]', '{r n kodu: 321447 zc 2321 fiyat: 14 95 usd kdv 58 99 tl kdv garanti: 12 ay stok: yok panlanan geli tarihi: 22 12 2017 planlanan geli tarihi nceden bildirilmeksizin de i tirilebilir}', 'r n kodu 321447 zc 2321 fiyat 14 95 usd kdv 58 99 tl kdv kdv dahil 17 64 usd 69 61 tl garanti 12 ay stok yok planlanan geli tarihi 22 12 2017 planlanan geli tarihi nceden bildirilmeksizin de i tirilebilir', 0.32635, 0.629),
              (-469, 77, 'hp pavilion dv7 4107eg lcd ekran 114991 sb 8937 dataservis net', 'None', 'Computers_and_Accessories', 'y zde y z uyum garant s detaylari n tiklayiniz 100 uyum garant s y zde y z uyum garant s ncelemekte oldu unuz r nde kopyala yap t r y ntemiyle hayali r n olu turan yap lardan korunmak amac yla temsili resim kullan lm t r yay nlad m z t m uyumluluk bilgileri uzman r n y neticilerimiz taraf ndan yap lan test ve kontroller neticesinde elde edilmekte ve uyum garantisi sa land ktan sonra yay na sunulmaktad r bu r n belirtilen model par a kodu ve r n a klamalar er evesinde cihaz n zla y zde y z uyumludur stisnai durumlarda uyumsuzlu un ispatlanmas ko uluyla hatal uyumsuz r n n geri g nderilmesi ve do ru r n n sevk edilmesiyle ilgili t m kargo giderleri firmam za aittir geri g nderimin anla mal oldu umuz kargo firmas ile yap lmas gerekmektedir durumu yeni r n boyut 17 3 z n rl k wxga piksel 1600 x 900 y zey parlak ayd nlatma led notlar', 'None', '[{/sku: [114991sb8937]}]', '{bulundu u depolar stok merkez: merkez outlet: kadik y 0 216 550 71 42: r n kodu: 114991 sb 8937 fiyat: 61 48 usd kdv 242 60 tl kdv garanti: 12 ay: stok: var}', 'bulundu u depolar stok merkez merkez outlet kadik y 0 216 550 71 42 g ncellenme 23 11 2017 05 02 08 r n kodu 114991 sb 8937 fiyat 61 48 usd kdv 242 60 tl kdv kdv dahil 72 55 usd 286 27 tl garanti 12 ay stok var', 0.5, 0.125),
              (-471, 77, 'hp photosmart 7850 cartridges for ink jet printers quill com', 'None', 'Office_Products', 'yields up to 175 pageshp 93 cartridge is not compatible with hp officejet 6310 all in one printer hp officejet 6310v all in one hp officejet 6310xi all in onefade resistant color provides superior results and brilliant true to life images that last for generations', 'None', '[{/productID: [901c9361wn]}]', 'None', 'None', 0.24454, 0.629); 
    """,

    'IUD_2_rollback': """
    INSERT INTO offers_setup (id, cluster_id, title, brand, category, description, price, identifiers, keyvaluepairs, spectablecontent, world_prob, attribute_prob)
    SELECT * FROM bulk_insert;	
    """,

    'IUD_3_rollback': """
    UPDATE offers 
    SET world_prob = 0.345,
        attribute_prob = 0.3992	
    WHERE _d0 = 615777
    AND _d1 = 613619;
    
    UPDATE offers 
    SET world_prob = 0.345,
        attribute_prob = 0.6008	
    WHERE _d0 = 615777
    and _d1 = 613841;
    
    UPDATE offers 
    SET world_prob = 0.1254,
        attribute_prob = 0.5	
    WHERE _d0 = 615999
    AND _d1 = 613619;
    
    UPDATE offers 
    SET world_prob = 0.1254,
        attribute_prob = 0.5
    WHERE _d0 = 615999
    and _d1 = 613841;
    
    UPDATE offers 
    SET world_prob = 0.487,
        attribute_prob = 0.4300
    WHERE _d0 = 615850
    and _d1 = 613395;
    
    UPDATE offers 
    SET world_prob = 0.487,
        attribute_prob = 0.5700	
    WHERE _d0 = 615850
    AND _d1 = 613692;
    
    UPDATE offers 
    SET world_prob = 0.487,
        attribute_prob = 0.4300
    WHERE _d0 = 615999
    and _d1 = 613841;
    
    UPDATE offers 
    SET world_prob = 0.487
    WHERE _d0 = 615553
    AND _d1 = 613692;
    
    UPDATE offers 
    SET world_prob = 0.487
    WHERE _d0 = 615553
    and _d1 = 613395;
    
    UPDATE offers 
    SET world_prob = 0.329
    WHERE _d0 = 614032
    AND _d1 = 612733;
    
    UPDATE offers 
    SET world_prob = 0.329
    WHERE _d0 = 614032
    and _d1 = 611874;
    
    UPDATE offers 
    SET world_prob = 0.184
    WHERE _d0 = 615197
    AND _d1 = 612733;
    
    UPDATE offers 
    SET world_prob = 0.184
    WHERE _d0 = 615197
    and _d1 = 613039;
    """,

    'IUD_4_rollback': """
    UPDATE offers_setup 
    SET cluster_id = max_cluster.max_id,
        world_prob = 1,
        attribute_prob = 1
    FROM (
        SELECT max(cluster_id) + 1 AS max_id
        FROM offers_setup   
    ) as max_cluster
    WHERE id = 12071001;
    
    UPDATE offers_setup 
    SET cluster_id = max_cluster.max_id,
        world_prob = 1,
        attribute_prob = 1
    FROM (
        SELECT max(cluster_id) + 1 AS max_id
        FROM offers_setup
    ) as max_cluster
    WHERE id = 16457529;
    
    UPDATE offers_setup 
    SET world_prob = 0.63,
        attribute_prob = 0.5
    WHERE id = 7339350;
    
    UPDATE offers_setup 
    SET world_prob = 0.63,
        attribute_prob = 0.5
    WHERE id = 12326926; 
    """,

    'IUD_5_rollback': """
    DELETE FROM offers_setup 
    WHERE cluster_id = 41;  
    """,

    'IUD_repairkey': """  
    DROP TABLE IF EXISTS offers_rk_world CASCADE; 
    DROP TABLE IF EXISTS offers_rk_attrs CASCADE; 
    DROP TABLE IF EXISTS offers CASCADE; 
    
    CREATE TABLE offers_rk_world AS REPAIR KEY cluster_id IN offers_setup WEIGHT BY world_prob;
    CREATE TABLE offers_rk_attrs AS REPAIR KEY id IN offers_setup WEIGHT BY attribute_prob;
    
    CREATE TABLE offers AS (
        SELECT attrs.* 
        FROM offers_rk_attrs AS attrs, offers_rk_world AS world
        WHERE attrs.id = world.id 
    );
    """
}

