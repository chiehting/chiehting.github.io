FROM ${RepositoryUri}rust:1.58.1-alpine3.15 as builder
WORKDIR /app
COPY . .
ENV RUST_BACKTRACE=full
RUN apk add --no-cache build-base eudev-dev linux-headers && \
RUN apk add --no-cache build-base eudev-dev linux-headers musl-dev python3-dev && \

  apt install libudev-dev pkg-config

cargo build --release -Z timings
--verbose
cargo clean && RUSTC_BOOTSTRAP=1 cargo build --release -Z timings
cargo clean && RUSTC_BOOTSTRAP=1 RUSTFLAGS="-Z time-passes" cargo build
cargo clean && RUSTC_BOOTSTRAP=1 cargo build --release --quiet -Z timings
cargo clean && strace -f -e execve -- cargo build --quiet 2>&1 | grep -E 'execve\(.*= 0'
cargo clean && RUSTFLAGS="-C link-args=-fuse-ld=lld" strace -f -e execve -- cargo build --quiet 2>&1 | grep -E 'execve\(.*= 0'
FROM ${RepositoryUri}alpine:3.15.0
ARG version
ENV version=$version
MAINTAINER justin
COPY --from=builder /app/target/release/spl-token /opt/main
WORKDIR /opt
ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ./main

