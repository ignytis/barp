function id()
    return "docker"
end

function build(args, env)
    -- base args
    local out_args = {"docker", "run", "--rm"}
    -- add env vars
    for k, v in pairs(env) do
        table.insert(out_args, "-e")
        table.insert(out_args, k .. "=" .. v)
    end
    -- add Docker image
    table.insert(out_args, "alpine:3.21")
    -- add command-line arguments
    for i, v in ipairs(args) do
        table.insert(out_args, v)
    end

    return {
        args=out_args,
        env={}
    }
end