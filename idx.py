import render

render.NewSprite([100,100,100,0,0,0,0,100,100,100], "red", 0,0, "sprite1")
render.NewSprite([100,100,100,0,0,0,0,100,100,100], "red", -200,0, "sprite2")

render.DrawAxis()

sprite1 = render.GetObj("sprite1")
sprite2 = render.GetObj("sprite2")
movedir1 = 1
movedir2 = 1

while True:
    render.clear(1)
    render.clear(2)

    sprite1.move(20 * movedir1,0)
    sprite2.move(40 * movedir2,0)

    print(sprite1.CheckCollisions("sprite2"), sprite1.CheckCollisions(False))

    if sprite1.CheckCollisions("x-axis") or sprite1.CheckCollisions(False) != 0:
        movedir1 *= -1

    if sprite2.CheckCollisions("x-axis") or sprite2.CheckCollisions(False) != 0:
        movedir2 *= -1
    
    render.RenderAll(1)
    # render.ShowAllHitBox()

