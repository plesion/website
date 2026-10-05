#!/usr/bin/env python3
"""Builds the translated home pages from the English one.

index.html (English) is the source. For each language below, this script copies it to
<lang>/index.html, swaps every English string for its translation, and fills in the
footer language switcher on every home page, English included.

Run it from the repository root after any change to index.html:

    python3 _i18n/build.py

It stops with an error if an English string it expects is no longer in index.html,
so a wording change on the English page can't silently leave a translation behind.
Jekyll (GitHub Pages) does not publish folders starting with an underscore, so this
folder stays out of the live site.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://plesion.com'

# Every language in the switcher: code, path, name in its own language, and the switcher's own words.
LANGS = [
    ('en', '/', 'English', 'Language', 'Choose a language', 'Close'),
    ('fr', '/fr/', 'Français', 'Langue', 'Choisir une langue', 'Fermer'),
    ('it', '/it/', 'Italiano', 'Lingua', 'Scegli una lingua', 'Chiudi'),
]

GLOBE = ('<svg class="lang-globe" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.6">'
         '<circle cx="12" cy="12" r="9.2"/><ellipse cx="12" cy="12" rx="4" ry="9.2"/><path d="M3 12h18M4.6 7h14.8M4.6 17h14.8"/></g></svg>')
CHECK = ('<svg class="lang-check" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2"/></svg>')


def switcher(cur):
    _, _, name, word, choose, close = next(l for l in LANGS if l[0] == cur)
    items = ''.join(
        '<li><a href="%s" lang="%s" hreflang="%s" data-lang="%s"%s>%s%s</a></li>'
        % (path, code, code, code, ' aria-current="true"' if code == cur else '', label, CHECK if code == cur else '')
        for code, path, label, *_ in LANGS)
    return ('<!-- lang:switch --><div class="lang">'
            '<button class="lang-btn" type="button" aria-expanded="false" aria-controls="lang-panel" aria-label="%s: %s">%s<span>%s</span></button>'
            '<div class="lang-panel" id="lang-panel" role="dialog" aria-label="%s" tabindex="-1" hidden>'
            '<div class="lang-head"><p>%s</p><button class="lang-close" type="button" aria-label="%s">×</button></div>'
            '<ul>%s</ul></div><div class="lang-veil" hidden></div></div><!-- /lang:switch -->'
            % (word, name, GLOBE, name, choose, choose, close, items))


# English HTML fragment -> translation. Fragments are matched exactly as they appear in index.html.
T = {
 'fr': [
  ('<title>PLESION | Real life. Around you. Here. Now.</title>', '<title>PLESION | La vraie vie. Autour de vous. Ici. Maintenant.</title>'),
  ('content="PLESION | Real life. Around you. Here. Now."', 'content="PLESION | La vraie vie. Autour de vous. Ici. Maintenant."'),
  ('content="The PLESION app shows what\'s happening around you, right now. Go live it."', 'content="L\'appli PLESION vous montre ce qui se passe autour de vous, en ce moment. Allez-y."'),
  ('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="fr_FR">'),
  ('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Aller au contenu</a>'),
  ('<p class="live-eyebrow">The live layer</p>', '<p class="live-eyebrow">Le réel en direct</p>'),
  ('<span>See</span> <span>what\'s</span> <span>alive</span> <span>around</span> <span>you.</span>',
   '<span>Voyez</span> <span>ce</span> <span>qui</span> <span>bouge</span> <span>autour</span> <span>de</span> <span>vous.</span>'),
  ('The city is alive. PLESION shows you where.', 'La ville est vivante. PLESION vous montre où.'),
  ('<img src="/assets/badge-app-store.svg" alt="Download on the App Store" width="120" height="40">', '<img src="/assets/badge-app-store-fr.svg" alt="Télécharger dans l\'App Store" width="127" height="40">'),
  ('<img src="/assets/badge-google-play.svg" alt="Get it on Google Play" width="135" height="40">', '<img src="/assets/badge-google-play-fr.svg" alt="Disponible sur Google Play" width="135" height="40">'),
  ('aria-label="At dusk, a woman on a terrace above a city of lights holds her phone, with posts for live jazz, an outdoor film and a night market pinned across the view."',
   'aria-label="Au crépuscule, sur une terrasse dominant une ville illuminée, une femme tient son téléphone ; des publications pour un concert de jazz, un film en plein air et un marché de nuit sont épinglées dans le paysage."'),
  ('aria-label="Here, now, for me, nearby"', 'aria-label="Ici, maintenant, pour moi, autour"'),
  ('<span class="ns-light" aria-hidden="true"></span>Here</p>', '<span class="ns-light" aria-hidden="true"></span>Ici</p>'),
  ('<span class="ns-light" aria-hidden="true"></span>Now</p>', '<span class="ns-light" aria-hidden="true"></span>Maintenant</p>'),
  ('<span class="ns-light" aria-hidden="true"></span>For me</p>', '<span class="ns-light" aria-hidden="true"></span>Pour moi</p>'),
  ('<span class="ns-light" aria-hidden="true"></span>Nearby</p>', '<span class="ns-light" aria-hidden="true"></span>Autour</p>'),
  ('Where you actually are.', 'Là où vous êtes vraiment.'),
  ('When something is actionable.', 'Quand vous pouvez en profiter.'),
  ('What makes it relevant.', 'Ce qui compte pour vous.'),
  ('<span class="ns-lite">10 min walk</span>', '<span class="ns-lite">10 min à pied</span>'),
  ('Ranked from near to far.', 'Du plus proche au plus loin.'),
  ('<p class="live-eyebrow">Time to reality</p>', '<p class="live-eyebrow">Place au réel</p>'),
  ('<span>Open.</span> <span>Discover.</span> <span>Go.</span>', '<span>Ouvrez.</span> <span>Trouvez.</span> <span>Sortez.</span>'),
  ('The app gets out of the way and the real world takes over.', 'L\'appli s\'efface et le monde réel prend le relais.'),
  ('aria-label="A man on a cobbled street by a bridge looks at his phone, with posts for live jazz, an outdoor film, a gallery opening and a night market floating at the places where they happen. Brooklyn, New York."',
   'aria-label="Dans une rue pavée près d\'un pont, un homme regarde son téléphone ; des publications pour un concert de jazz, un film en plein air, un vernissage et un marché de nuit flottent là où ils ont lieu. Brooklyn, New York."'),
  ('aria-label="PLESION: here, now, for you"', 'aria-label="PLESION : ici, maintenant, pour vous"'),
  ('<span class="l l1">Here.</span> <span class="l l2">Now.</span> <span class="l l3">For you<span',
   '<span class="l l1">Ici.</span> <span class="l l2">Maintenant.</span> <span class="l l3">Pour vous<span'),
  ('<p class="live-eyebrow">Physical relevance</p>', '<p class="live-eyebrow">Pertinence physique</p>'),
  ('<span>Real</span> <span>is</span> <span>good.</span>', '<span>Vive</span> <span>le</span> <span>réel.</span>'),
  ('Escape the endless scroll. PLESION helps you enjoy real life with real people.',
   'Sortez du scroll sans fin. PLESION vous aide à profiter de la vraie vie, avec de vraies personnes.'),
  ('aria-label="A young man with a backpack looks out at sunset over a city of brick buildings and street murals, phone in hand, with posts for live jazz, an outdoor film, a gallery opening and a night market pinned across the view."',
   'aria-label="Au coucher du soleil, un jeune homme avec un sac à dos, téléphone en main, regarde une ville de briques et de fresques ; des publications pour un concert de jazz, un film en plein air, un vernissage et un marché de nuit sont épinglées dans le paysage."'),
  ('class="footer-logo" href="/" aria-label="PLESION home"', 'class="footer-logo" href="/fr/" aria-label="Accueil PLESION"'),
  ('<span>Real life. Around you.</span> <span>Here. Now.</span>', '<span>La vraie vie. Autour de vous.</span> <span>Ici. Maintenant.</span>'),
  ('aria-label="PLESION on social media and app stores"', 'aria-label="PLESION sur les réseaux sociaux et les boutiques d\'applications"'),
  ('>News on Instagram<', '>Actualités sur Instagram<'),
  ('>Videos on TikTok<', '>Vidéos sur TikTok<'),
  ('>News on Facebook<', '>Actualités sur Facebook<'),
  ('>News on X<', '>Actualités sur X<'),
  ('>Company news on LinkedIn<', '>L\'entreprise sur LinkedIn<'),
  ('>Insights on Medium<', '>Analyses sur Medium<'),
  ('<nav aria-label="Legal">', '<nav aria-label="Mentions légales">'),
  ('<a href="/data-policy">Data policy</a>', '<a href="/data-policy" hreflang="en">Politique de données</a>'),
  ('<a href="/terms-of-service">Terms of service</a>', '<a href="/terms-of-service" hreflang="en">Conditions d\'utilisation</a>'),
 ],
 'it': [
  ('<title>PLESION | Real life. Around you. Here. Now.</title>', '<title>PLESION | La vita reale. Intorno a te. Qui. Ora.</title>'),
  ('content="PLESION | Real life. Around you. Here. Now."', 'content="PLESION | La vita reale. Intorno a te. Qui. Ora."'),
  ('content="The PLESION app shows what\'s happening around you, right now. Go live it."', 'content="L\'app PLESION ti mostra cosa succede intorno a te, adesso. Vai a viverlo."'),
  ('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="it_IT">'),
  ('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Vai al contenuto</a>'),
  ('<p class="live-eyebrow">The live layer</p>', '<p class="live-eyebrow">Il reale in diretta</p>'),
  ('<span>See</span> <span>what\'s</span> <span>alive</span> <span>around</span> <span>you.</span>',
   '<span>Scopri</span> <span>cosa</span> <span>succede</span> <span>intorno</span> <span>a</span> <span>te.</span>'),
  ('The city is alive. PLESION shows you where.', 'La città è viva. PLESION ti mostra dove.'),
  ('<img src="/assets/badge-app-store.svg" alt="Download on the App Store" width="120" height="40">', '<img src="/assets/badge-app-store-it.svg" alt="Scarica su App Store" width="120" height="40">'),
  ('<img src="/assets/badge-google-play.svg" alt="Get it on Google Play" width="135" height="40">', '<img src="/assets/badge-google-play-it.svg" alt="Disponibile su Google Play" width="135" height="40">'),
  ('aria-label="At dusk, a woman on a terrace above a city of lights holds her phone, with posts for live jazz, an outdoor film and a night market pinned across the view."',
   'aria-label="Al tramonto, su una terrazza sopra una città illuminata, una donna tiene in mano il telefono; post per un concerto jazz, un film all\'aperto e un mercato notturno sono appuntati nel panorama."'),
  ('aria-label="Here, now, for me, nearby"', 'aria-label="Qui, ora, per me, vicino"'),
  ('<span class="ns-light" aria-hidden="true"></span>Here</p>', '<span class="ns-light" aria-hidden="true"></span>Qui</p>'),
  ('<span class="ns-light" aria-hidden="true"></span>Now</p>', '<span class="ns-light" aria-hidden="true"></span>Ora</p>'),
  ('<span class="ns-light" aria-hidden="true"></span>For me</p>', '<span class="ns-light" aria-hidden="true"></span>Per me</p>'),
  ('<span class="ns-light" aria-hidden="true"></span>Nearby</p>', '<span class="ns-light" aria-hidden="true"></span>Vicino</p>'),
  ('Where you actually are.', 'Dove sei davvero.'),
  ('When something is actionable.', 'Quando puoi approfittarne.'),
  ('What makes it relevant.', 'Ciò che conta per te.'),
  ('<span class="ns-lite">10 min walk</span>', '<span class="ns-lite">10 min a piedi</span>'),
  ('Ranked from near to far.', 'Dal più vicino al più lontano.'),
  ('<p class="live-eyebrow">Time to reality</p>', '<p class="live-eyebrow">Spazio al reale</p>'),
  ('<span>Open.</span> <span>Discover.</span> <span>Go.</span>', '<span>Apri.</span> <span>Scopri.</span> <span>Vai.</span>'),
  ('The app gets out of the way and the real world takes over.', 'L\'app si fa da parte e il mondo reale prende il sopravvento.'),
  ('aria-label="A man on a cobbled street by a bridge looks at his phone, with posts for live jazz, an outdoor film, a gallery opening and a night market floating at the places where they happen. Brooklyn, New York."',
   'aria-label="In una strada acciottolata vicino a un ponte, un uomo guarda il telefono; post per un concerto jazz, un film all\'aperto, un\'inaugurazione e un mercato notturno fluttuano nei luoghi dove accadono. Brooklyn, New York."'),
  ('aria-label="PLESION: here, now, for you"', 'aria-label="PLESION: qui, ora, per te"'),
  ('<span class="l l1">Here.</span> <span class="l l2">Now.</span> <span class="l l3">For you<span',
   '<span class="l l1">Qui.</span> <span class="l l2">Ora.</span> <span class="l l3">Per te<span'),
  ('<p class="live-eyebrow">Physical relevance</p>', '<p class="live-eyebrow">Rilevanza fisica</p>'),
  ('<span>Real</span> <span>is</span> <span>good.</span>', '<span>Il</span> <span>reale</span> <span>è</span> <span>bello.</span>'),
  ('Escape the endless scroll. PLESION helps you enjoy real life with real people.',
   'Esci dallo scroll infinito. PLESION ti aiuta a goderti la vita reale con persone reali.'),
  ('aria-label="A young man with a backpack looks out at sunset over a city of brick buildings and street murals, phone in hand, with posts for live jazz, an outdoor film, a gallery opening and a night market pinned across the view."',
   'aria-label="Al tramonto, un ragazzo con lo zaino e il telefono in mano guarda una città di mattoni e murales; post per un concerto jazz, un film all\'aperto, un\'inaugurazione e un mercato notturno sono appuntati nel panorama."'),
  ('class="footer-logo" href="/" aria-label="PLESION home"', 'class="footer-logo" href="/it/" aria-label="Home PLESION"'),
  ('<span>Real life. Around you.</span> <span>Here. Now.</span>', '<span>La vita reale. Intorno a te.</span> <span>Qui. Ora.</span>'),
  ('aria-label="PLESION on social media and app stores"', 'aria-label="PLESION sui social e negli store"'),
  ('>News on Instagram<', '>Novità su Instagram<'),
  ('>Videos on TikTok<', '>Video su TikTok<'),
  ('>News on Facebook<', '>Novità su Facebook<'),
  ('>News on X<', '>Novità su X<'),
  ('>Company news on LinkedIn<', '>L\'azienda su LinkedIn<'),
  ('>Insights on Medium<', '>Approfondimenti su Medium<'),
  ('<nav aria-label="Legal">', '<nav aria-label="Note legali">'),
  ('<a href="/data-policy">Data policy</a>', '<a href="/data-policy" hreflang="en">Informativa sui dati</a>'),
  ('<a href="/terms-of-service">Terms of service</a>', '<a href="/terms-of-service" hreflang="en">Termini di servizio</a>'),
 ],
}

SWITCH_RE = re.compile(r'<!-- lang:switch -->.*?<!-- /lang:switch -->', re.S)


def webpage_jsonld(code, path, name, description):
    graph = {'@context': 'https://schema.org', '@graph': [{
        '@type': 'WebPage', '@id': SITE + path + '#webpage', 'url': SITE + path, 'name': name,
        'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#organization'},
        'description': description, 'inLanguage': code}]}
    return '<script type="application/ld+json">\n  ' + json.dumps(graph, ensure_ascii=False, indent=2).replace('\n', '\n  ') + '\n  </script>'


def main():
    src_path = os.path.join(ROOT, 'index.html')
    src = open(src_path, encoding='utf-8').read()
    if not SWITCH_RE.search(src):
        sys.exit('index.html has no <!-- lang:switch --> marker in the footer')
    src = SWITCH_RE.sub(lambda m: switcher('en'), src)
    open(src_path, 'w', encoding='utf-8').write(src)

    for code, path, *_ in LANGS[1:]:
        h = src
        missing = [en for en, _ in T[code] if en not in h]
        if missing:
            sys.exit('%s: these English strings are no longer in index.html:\n  %s' % (code, '\n  '.join(missing)))
        for en, tr in T[code]:
            h = h.replace(en, tr)
        h = h.replace('<html lang="en">', '<html lang="%s">' % code, 1)
        h = h.replace('<link rel="canonical" href="%s/">' % SITE, '<link rel="canonical" href="%s%s">' % (SITE, path), 1)
        h = h.replace('<meta property="og:url" content="%s/">' % SITE, '<meta property="og:url" content="%s%s">' % (SITE, path), 1)
        title = re.search(r'<title>(.*?)</title>', h).group(1)
        desc = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
        h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: webpage_jsonld(code, path, title, desc), h, count=1, flags=re.S)
        h = SWITCH_RE.sub(lambda m: switcher(code), h)
        os.makedirs(os.path.join(ROOT, code), exist_ok=True)
        open(os.path.join(ROOT, code, 'index.html'), 'w', encoding='utf-8').write(h)
        print('wrote %s/index.html' % code)


if __name__ == '__main__':
    main()
