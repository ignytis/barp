function id()
    return "docker"
end

function build(args)
    return {"docker", "run", "--rm", "alpine:3.21", table.unpack(args)}
end