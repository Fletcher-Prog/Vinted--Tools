const { MessageEmbed } = require("discord.js");


module.exports = {
    name: "ping",
    category: "utils",
    permissions: ["SEND_MESSAGES"],
    ownerOnly: false,
    usage: "ping",
    examples: ["ping"],
    description: "La commande ping renvoie la latence du bot et de l'API",
    async run(client, message, args) { // run c'est les commande avec le prefix !ping
        const tryPong = await message.reply({
            content: "On essaye de pong... un instant!",
            fetchReply: true,
        });

        const embed = new MessageEmbed()
            .setTitle("Pong! 🏓 ")
            .setThumbnail(client.user.displayAvatarURL({ dynamic: true, size: 1024 }))
            .addFields(
                {
                    name: "Latence API",
                    value: `\`\`\`${client.ws.ping}ms\`\`\``,
                    inline: true,
                },
                {
                    name: "Latence BOT",
                    value: `\`\`\`${tryPong.createdTimestamp - message.createdTimestamp
                        }ms\`\`\``,
                    inline: true,
                },
                {
                    name: "Uptime",
                    value: `<t:${parseInt(client.readyTimestamp / 1000)}:R>`,
                    inline: false
                }
            )
            .setColor("#f00020")
            .setTimestamp()
            .setFooter({
                text: message.author.username,
                iconURL: message.author.displayAvatarURL(),
            });

        tryPong.edit({ content: " ", embeds: [embed] });


    },
    async runInteraction(client, interaction) { //runInterac  c'est pour les commandes avec le /
        const tryPong = await interaction.reply({
            content: "On essaye de pong... un instant!",
            fetchReply: true,
        });

        const embed = new MessageEmbed()
            .setTitle("Pong! 🏓")
            .addFields(
                {
                    name: "Latence API",
                    value: `\`\`\`${client.ws.ping}ms\`\`\``,
                    inline: true,
                },
                {
                    name: "Latence BOT",
                    value: `\`\`\`${tryPong.createdTimestamp - interaction.createdTimestamp
                        }ms\`\`\``,
                    inline: true,
                },
                {
                    name: "Uptime",
                    value: `<t:${parseInt(client.readyTimestamp / 1000)}:R>`,
                    inline: false
                }
            )
            .setColor("#f00020")
            .setThumbnail(interaction.guild.iconURL({ dynamic: true, size: 1024 }))
            .setTimestamp()
            .setFooter({
                text: interaction.user.username,
                iconURL: interaction.user.displayAvatarURL(),
            });

        interaction.editReply({ content: " ", embeds: [embed] });
    }
}