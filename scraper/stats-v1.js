const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const readline = require('readline');

// Funkcja do wczytywania liczby stron od użytkownika
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Ile stron chcesz pobrać? ', (numberOfPages) => {
    numberOfPages = parseInt(numberOfPages, 10);
    if (isNaN(numberOfPages) || numberOfPages <= 0) {
        console.log('Proszę podać prawidłową liczbę stron.');
        rl.close();
        return;
    }

    // Start procesu scrapowania dla każdej strony
    scrapeMultiplePages(numberOfPages);
    rl.close();
});

async function scrapeMultiplePages(numberOfPages) {
    let allMemes = [];

    for (let i = 1; i <= numberOfPages; i++) {
        const url = `https://jbzd.com.pl/str/${i}`;
        console.log(`Scraping strony: ${url}`);
        const memesFromPage = await scrapeJbzd(url);
        allMemes = allMemes.concat(memesFromPage);
    }

    // Zapisz wszystkie dane do pliku JSON po przetworzeniu wszystkich stron
    fs.writeFileSync('data.json', JSON.stringify(allMemes, null, 2));
    console.log('Scraping completed. Data saved to data.json.');
}

async function scrapeJbzd(url) {
    try {
        // Pobieranie zawartości strony
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        // Tworzenie tablicy do przechowywania zebranych danych
        let memes = [];

        // Wybieranie wszystkich artykułów na stronie
        $('article.article').each((index, element) => {
            const title = $(element).find('.article-title a').text().trim();
            const link = $(element).find('.article-title a').attr('href')?.trim();

            // Pobieranie autora z atrybutu alt obrazka
            const parsedAuthor = $(element).find('.article-avatar img').attr('alt')?.trim() || '';

            // Pobieranie danych o monetach z content-badges-view
            const badgesAttr = $(element).find('content-badges-view').attr(':model-badge');
            let stone = 0, silver = 0, gold = 0, wyp = 0;
            if (badgesAttr) {
                try {
                    const badgesJSON = badgesAttr.replace(/&quot;/g, '"');
                    const parsedBadges = JSON.parse(badgesJSON);
                    stone = parsedBadges.stone;
                    silver = parsedBadges.silver;
                    gold = parsedBadges.gold;
                    wyp = parsedBadges.wyp;
                } catch (parseError) {
                    console.error('Error parsowania coinow:', parseError);
                }
            }

            const date = $(element).find('.article-time').attr('data-date')?.trim();
            const comments = $(element).find('.article-title-comments-count span').text().trim();
            const likes = $(element).find('.article-actions vote').attr(':score');

            // Składanie obiektu z danymi
            const meme = {
                title,
                link,
                author: parsedAuthor,
                coins: {
                    stone,
                    silver,
                    gold,
                    wyp
                },
                likes: likes ? parseInt(likes) : 0,
                comments: comments ? parseInt(comments) : 0,
                date
            };

            // Dodawanie obiektu do tablicy
            memes.push(meme);
        });

        return memes;
    } catch (error) {
        console.error('Error cos sie zjebalo:', error);
        return [];
    }
}
