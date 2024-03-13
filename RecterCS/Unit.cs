class Unit
{
    private
        string name;
        int health;
        int damage;
        int range;
    public
        Unit(
            string name,
            int health,
            int damage,
            int range
    ) {
        this.name = name;
        this.health = health;
        this.damage = damage;
        this.range = range;
    }
    public void getInfo()
    {
        Console.WriteLine($"{name} {health} {damage} {range}");
    }
}