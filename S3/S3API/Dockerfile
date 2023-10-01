#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["S3API/S3API.csproj", "S3API/"]
RUN dotnet restore "S3API/S3API.csproj"
COPY . .
WORKDIR "/src/S3API"
RUN dotnet build "S3API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "S3API.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "S3API.dll", "--console"]