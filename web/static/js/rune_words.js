$(() => {
    const runes = new $('#rune-filter').attr('data-runes').split('|');
    const n_cols = 4;
    let cur_p = undefined;
    runes.forEach((rune, i) => {
        if (i % n_cols === 0) {
            if (cur_p) $('#rune-filter').append(cur_p);
            cur_p = $('<p>');
        }
        const rune_n = rune.split(' ')[0];
        let cb = $(`<label><input type="checkbox" name="rune-cb" data-rune="${rune_n}"> ${rune} &nbsp;&nbsp;</label>`)
        cur_p.append(cb);
    })
    if (cur_p && cur_p.text()) $('#rune-filter').append(cur_p);

    $('[name=rune-cb]').change(() => {
        const checked_runes = [];
        $('[name=rune-cb]:checked').each((i, e) => {
            checked_runes.push($(e).attr('data-rune'));
        })
        const tr_rw = $('[data-type="tr-rune-word"]');
        tr_rw.show();
        if (checked_runes.length > 0) {
            tr_rw.each((i, e) => {
                const required = $(e).attr('data-runes').split(' ');
                if (!required.every(val => checked_runes.includes(val))) {
                    $(e).hide();
                }
            });
        }
    });
})
