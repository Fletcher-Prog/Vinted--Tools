const { MessageEmbed } = require("discord.js");

module.exports = {
    name: "say",
    category: "admin",
    permissions: ["ADMINISTRATOR"],
    ownerOnly: false,
    usage: "say",
    examples: ["say"],
    description: "Envoyer un message à la place du bot :",
    options: [
        {
            name: 'message',
            description: 'Message à envoyer à la place du bot :',
            type: 'STRING',
            required: true,
        }
    ],
    run(client, message, args) {
        if (message.author.bot) return;
        message.delete();
        const SayMessage = message.content.slice(4).trim();
        message.channel.send(SayMessage);

        //logs
        const logChannel = client.channels.cache.get(process.env.LOG_CHANNEL);
        let embedLog = new MessageEmbed()
            .setTitle("Logs des commandes")
            .setColor("FF0000")
            .setDescription(` ${message.author.tag} -->  **${this.name}**  :  __${SayMessage}`)
            .setTimestamp()
            .setFooter({ text: `${message.author.tag}`, iconURL: message.author.displayAvatarURL() })
        logChannel.send({ embeds: [embedLog] });
    },
    async runInteraction(client, interaction) {

        interaction.reply({ content: interaction.options.getString("message"), fetchReply: true });


        //logs
        const logChannel = client.channels.cache.get(process.env.LOG_CHANNEL); 
        let embedLog = new MessageEmbed()
        .setTitle("Logs des commandes")
        .setColor("FF0000")
        .setDescription(` ${interaction.user.tag} -->  **${this.name}**  :  __${interaction.options.getString("message")}__ `)
        .setTimestamp()
        .setFooter({ text: `${interaction.user.tag}`, iconURL: interaction.user.displayAvatarURL() })
        logChannel.send({embeds : [embedLog]});
    }

}