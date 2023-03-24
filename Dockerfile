FROM alpine:3.16

RUN apk add --no-cache go hugo git make perl
RUN go install github.com/jackyzha0/hugo-obsidian@latest
ENV PATH="/root/go/bin:$PATH"

RUN git config --global --add safe.directory /quartz

WORKDIR /quartz

CMD ["make", "serve"]
