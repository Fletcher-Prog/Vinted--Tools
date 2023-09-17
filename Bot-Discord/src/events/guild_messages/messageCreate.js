const ownerId = require('../../../config.json').ownerId;
const prefix = process.env.PREFIX;

module.exports = {
    name: 'messageCreate',
    once: false,
    execute(client, message) {
        if (message.author.bot) return;
        if (!message.content.startsWith(prefix)) return;

        const args = message.content.slice(prefix.length).trim().split(/ +/g);
        const cmdName = args.shift().toLowerCase();
        if (cmdName.length == 0) return;

        let cmd = client.commands.get(cmdName);
        if (!cmd) return;

        if (cmd.ownerOnly) {
            if (!ownerId.includes(message.author.id)) return message.reply("La seule personne pouvant taper cette commande est l'owner du bot !");
        }

        if (!message.member.permissions.has([cmd.permission])) return message.reply(`Vous n'avez pas la/les permission(s) requise(s) (\`${cmd.permission.join(', ')}\`) pour taper cette commande:`);

        
        if (cmd) cmd.run(client, message, args);
    },
};


