async function url_down(url) {
    const res = await fetch(url);
    let data = await res.json();
    return data;
}

async function main() {
    let dataOut = await url_down('http://127.0.0.1:5000/vinted?https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first');
}

main();



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!addlink'):
        channel = discord.utils.get(client.channels, name=message.channel) 
        print((channel))
        await channel.send('Hello!') 